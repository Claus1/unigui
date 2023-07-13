from aiohttp import web, WSMsgType
from .user import *
from config import port, pretty_print, socket_ip, socket_port, upload_dir
from pathlib import Path
from .reloader import empty_app 

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
        
    return web.HTTPNotFound() if not file_path.exists() else (web.FileResponse(file_path)     
         if request.path != User.fix_file else web.Response(text = User.fixed_main)) 

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    user = User.UserType()

    async def send(res):
        await ws.send_str(jsonString(user.prepare_result(res)))        
    user.send = send 
    
    ok = user.load()
    
    await ws.send_str(jsonString(user.screen if ok else empty_app)) 

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                data = json.loads(msg.data)            
                result = user.result4message(data)
                if result:                
                    await ws.send_str(jsonString(user.prepare_result(result)))
        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                ws.exception())

    print('websocket connection closed')
    return ws       

def start(appname, user_type = User, translate_path = None, http_handlers = []):
    
    set_utils(appname, port, upload_dir, translate_path, socket_ip, socket_port)    
    
    if upload_dir and not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    User.UserType = user_type

    if socket_ip != 'localhost' or resource_port != 8000 or socket_port != 1234:
        User.create_fixed_js()     
        http_handlers.append(web.get(User.fix_file, static_serve))
    else:
        User.fix_file = None
    
    http_handlers.insert(0, web.get('/ws', websocket_handler))
        
    for h in [web.get('/', static_serve), 
        web.static('/js', f"{webpath}/js"),
        web.static('/fonts', f"{webpath}/fonts"),
        web.static('/css', f"{webpath}/css"),
        web.static('/icons', f"{webpath}/icons"),
        web.static(f'/{upload_dir}', f"/{app_user_dir}/{upload_dir}"),
        web.post('/', post_handler)]:

        http_handlers.append(h)

    print(f'Start {appname} server on {port} port..')    
    app = web.Application()
    app.add_routes(http_handlers)    
    web.run_app(app,  port=port)
    
