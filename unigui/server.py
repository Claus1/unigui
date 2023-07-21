from aiohttp import web, WSMsgType
from .users import *
from pathlib import Path
from .reloader import empty_app 
from .autotest import recorder, jsonString, run_tests
from config import port, upload_dir
from .utils import app_dir
import traceback

async def post_handler(request):
    reader = await request.multipart()
    field = await reader.next()   
    filename = upload_path(field.filename)      
    size = 0
    with open(filename, 'wb') as f:
        while True:
            chunk = await field.read_chunk()  
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    return web.Response(text=filename)

async def static_serve(request):    
    file_path = request.path    
    file_path  = Path(f"{webpath}{file_path}" )
    if request.path == '/':
        file_path /= 'index.html' 
    
    answer = web.HTTPNotFound() if not file_path.exists() else web.FileResponse(file_path)          
    return answer

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    user = User.UserType()

    async def send(res):
        res = jsonString(user.prepare_result(res))
        await ws.send_str(res)   

    user.send = send     
    user.session__ = request.remote
    ok = user.load()    
    await ws.send_str(jsonString(user.screen if ok else empty_app)) 

    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    data = json.loads(msg.data)            
                    result = user.result4message(data)
                    if result:            
                        result = user.prepare_result(result)
                        await ws.send_str(jsonString(result))
                    recorder(data, result)

            elif msg.type == WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())
    except:        
        user.log(traceback.format_exc())
    return ws       

def start(appname = '', user_type = User, http_handlers = []):
    if appname:
        config.appname = appname

    User.UserType = user_type    

    if config.autotest:
        run_tests()

    http_handlers.insert(0, web.get('/ws', websocket_handler))        
    for h in [web.static(f'/{config.upload_dir}', f"/{app_dir}/{upload_dir}"), 
        web.get('/{tail:.*}', static_serve), web.post('/', post_handler)]:
        http_handlers.append(h)

    print(f'Start {appname} server on {port} port..')    
    app = web.Application()
    app.add_routes(http_handlers)    
    web.run_app(app,  port=port)
    
