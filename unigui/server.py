from aiohttp import web, WSMsgType
from .users import *
from pathlib import Path
from .reloader import empty_app 
from .autotest import recorder, jsonString, run_tests
from config import port, upload_dir
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

def broadcast(message, message_user):
    screen = message_user.screen_module
    for user in User.reflections:
        if user is not message_user and screen is user.screen_module:
            user.sync_send(message)

def screen_switch_message(message):
    return len(message) == 2 and message[0] == 'root'

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    user, ok = make_user()

    async def send(res):
        if type(res) != str:
            res = jsonString(user.prepare_result(res))
        await ws.send_str(res)   

    user.send = send     
    user.session = request.remote    
    await send(user.screen if ok else empty_app) 
    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    input = json.loads(msg.data)            
                    result = user.result4message(input)
                    if result:                                    
                        await send(result)
                    if recorder.record_file:
                        recorder.accept(input, result)
                    if config.mirror and not screen_switch_message(input):                        
                        if result:
                            broadcast(result, user)                            
                        msg_object = user.find_element(input)                         
                        if not isinstance(result, Message) or not result.contains(msg_object):                                                        
                            broadcast(jsonString(user.prepare_result(msg_object)), user)
            elif msg.type == WSMsgType.ERROR:
                user.log('ws connection closed with exception %s' % ws.exception())
    except:        
        user.log(traceback.format_exc())

    if User.reflections:
        User.reflections.remove(user)
    return ws       

def start(appname = '', user_type = User, http_handlers = []):
    if appname:
        config.appname = appname

    User.UserType = user_type    

    if config.autotest:
        run_tests()

    http_handlers.insert(0, web.get('/ws', websocket_handler))        
    http_handlers += [web.static(f'/{config.upload_dir}', upload_dir), 
        web.get('/{tail:.*}', static_serve), web.post('/', post_handler)]

    print(f'Start {appname} web server..')    
    app = web.Application()
    app.add_routes(http_handlers)    
    web.run_app(app,  port=port)
    
