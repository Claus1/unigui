from aiohttp import web, WSMsgType
from .users import *
from pathlib import Path
from .reloader import empty_app 
from .autotest import recorder, jsonString, run_tests
from .common import  *
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
    rpath = request.path    
    file_path  = Path(f"{webpath}{rpath}" )
    if request.path == '/':
        file_path /= 'index.html'

    if not file_path.exists():
        file_path = None
        #unmask win path
        if rpath.startswith('/') and rpath[2] == ':':
            rpath = rpath[1:]
        dirs = getattr(config, public_dirs, []) 
        for dir in dirs:              
            if rpath.startswith(dir):                
                if os.path.exists(rpath):
                    file_path  = Path(rpath)
                break
            
    return web.FileResponse(file_path) if file_path else web.HTTPNotFound()
     
def broadcast(message, message_user):
    screen = message_user.screen_module
    for user in User.reflections:
        if user is not message_user and screen is user.screen_module:
            user.sync_send(message)

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    user, ok = make_user()
    user.transport = ws._writer.transport  if divpath != '/' else None          

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
                    raw_message = json.loads(msg.data)
                    if isinstance(raw_message, list):
                        for raw_submessage in raw_message:
                            message = ReceivedMessage(raw_submessage)                    
                            result = user.result4message(message)
                        else:                        
                            message = None
                            result = Error('Empty command batch!')
                    else:                    
                        message = ReceivedMessage(raw_message)            
                        result = user.result4message(message)                    
                    await send(result)
                    if message:
                        if recorder.record_file:
                            recorder.accept(message, result)
                        if config.mirror and not is_screen_switch(message):                        
                            if result:
                                broadcast(result, user)                            
                            msg_object = user.find_element(message)                         
                            if not isinstance(result, Message) or not result.contains(msg_object):                                                        
                                broadcast(jsonString(user.prepare_result(msg_object)), user)
            elif msg.type == WSMsgType.ERROR:
                user.log('ws connection closed with exception %s' % ws.exception())
    except:        
        user.log(traceback.format_exc())

    if User.reflections:
        User.reflections.remove(user)
    return ws       

def start(appname = None, user_type = User, http_handlers = []):    
    if appname is not None:
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
    
