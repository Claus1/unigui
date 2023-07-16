from aiohttp import web, WSMsgType
from .users import *
from config import port, pretty_print, socket_ip, upload_dir
from pathlib import Path
from .reloader import empty_app 
from .autotest import recorder

async def post_handler(request):
    reader = await request.multipart()
    field = await reader.next()   
    filename = upload_path(field.filename)  
    # You cannot rely on Content-Length if transfer is chunked.
    size = 0
    with open(filename, 'wb') as f:
        while True:
            chunk = await field.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    return web.Response(text=f'{filename} sized of {size} successfully stored')

def jsonString(obj):
    return toJson(obj, 2 if pretty_print else 0, pretty_print)

async def static_serve(request):    
    file_path = request.path
    if upload_dir not in  request.path:
        file_path = f"{webpath}{file_path}"  # rebase into static dir
    file_path  = Path(file_path)
    
    if request.path == '/':
        file_path /= 'index.html'
        
    answer = web.HTTPNotFound() if not file_path.exists() else (web.FileResponse(file_path)     
         if request.path != User.fix_file else web.Response(text = User.fixed_main)) 

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
                        result = jsonString(user.prepare_result(result))    
                        await ws.send_str(result)
                    recorder(msg.data, result)

            elif msg.type == WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())
    except:
        type, value, traceback = sys.exc_info()
        user.log(f'{type}: {value} \n{traceback.format_exc()}\n')
    
    return ws       

def start(appname, user_type = User, http_handlers = []):
    
    set_utils(appname, port, upload_dir, socket_ip)    
    
    if upload_dir and not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    User.UserType = user_type    
    User.create_fixed_js()      
    http_handlers.insert(0, web.get('/ws', websocket_handler))
        
    for h in [web.get('/{tail:.*}', static_serve), web.post('/', post_handler)]:
        http_handlers.append(h)

    print(f'Start {appname} server on {port} port..')    
    app = web.Application()
    app.add_routes(http_handlers)    
    web.run_app(app,  port=port)
    
