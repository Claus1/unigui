from aiohttp import web, WSMsgType
import asyncio
import traceback
from . import utils

import os
import cgi
from .manager import * 
import requests

class UniHandler:    
    def log_message(self, format, *args):
        return

    def translate_path(self, path):        
        return utils.translate_path(path)

    @staticmethod
    def cache_name(url):    
        name = url.split('/')[-1]
        name = utils.upload_path(name)
        return name
        
    @staticmethod
    def cache_url(url):
        "returns cached name of url image"
        cname = UniHandler.cache_name(url)
        if not os.path.exists(cname):
            response = requests.get(url)
            if response.status_code != 200:
                return None
            file = open(cname, "wb")
            file.write(response.content)
            file.close() 
        return cname

    @staticmethod
    def create_fixed_js():
        dir = f"{utils.webpath}/js"        
        for file in os.listdir(dir):
            fn = f'{dir}/{file}'
            if file[0].isdigit() and file.endswith(".js") and os.path.getsize(fn) > 25000:
                UniHandler.fix_file = f'/js/{file}'
                with open(fn, 'rb') as main:
                    b = main.read()
                    if utils.socket_ip != 'localhost':
                        b = b.replace(bytes('localhost',encoding='utf8'), bytes(str(utils.socket_ip),encoding='utf8'))                
                    if utils.resource_port != 8000:
                        b = b.replace(bytes('8000',encoding='utf8'), bytes(str(utils.resource_port),encoding='utf8'))                
                    if utils.socket_port != 1234:
                        b = b.replace(bytes('1234',encoding='utf8'), bytes(str(utils.socket_port),encoding='utf8'))                
                    UniHandler.fixed_main = b.decode("utf-8") 
                    print(f"Fixed {file} created on ip {utils.socket_ip}, http port {utils.resource_port}, socket port {utils.socket_port}.")
                    break

    def deal_post_data(self):
        ctype, _ = cgi.parse_header(self.headers['Content-Type'])
        if ctype == 'multipart/form-data':
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ =
                {'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'],})            
            try:
                fs = form.list[0]
                fn = upload_path(fs.filename) 
                open(fn, "wb").write(fs.file.read())
            except IOError:
                return (False, "Can't create file to write, do you have permission to write?")
            return (True, "Files uploaded")

        return (False,f'Invalide header type {ctype}!')

from config import port, user_dir, pretty_print, socket_ip, socket_port, upload_dir
from pathlib import Path

async def static_serve(request):
    if "Upgrade" in request.headers and request.headers["Upgrade"] == 'websocket':
        return await websocket_handler(request)
    file_path = request.path
    if upload_dir not in  request.path:
        file_path = f"{utils.webpath}{file_path}"  # rebase into static dir
    file_path  = Path(file_path)
    
    if request.path == '/':
        file_path /= 'index.html'
        
    if not file_path.exists():
        return web.HTTPNotFound()
     
    return web.FileResponse(file_path) if request.path != UniHandler.fix_file else web.Response(text = UniHandler.fixed_main) 

async def websocket_handler(request):

        ws = web.WebSocketResponse()
        await ws.prepare(request)

        def jsonString(obj):
            return toJson(obj, 0, False)
        
        user = User()
        async def send(res):
            await ws.send_str(jsonString(user.prepare_result(res)))
            #await asyncio.sleep(1)
        user.send = send 
        user.load()
        
        await ws.send_str(jsonString([user.menu,user.screen])) 

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

def start(appname, user_type = User, httpHandler = UniHandler, translate_path = None, http_handlers = []):
    wd = os.getcwd()
    import sys
    sys.path.insert(0,wd) #load from working directory
    
    sys.path.pop(0) #delete work path

    set_utils(appname,user_dir, port, upload_dir, translate_path, socket_ip, socket_port)    

    if utils.socket_ip != 'localhost' or utils.resource_port != 8000 or utils.socket_port != 1234:
        UniHandler.create_fixed_js()     
        #http_handlers.insert(0, web.get(UniHandler.fix_file, serve_fixed))   
    else:
        UniHandler.fix_file = None
    

    """ 
    async def session(websocket, path):
        address = websocket.remote_address
        try:            
            if address in users:
                user = users[address]
            else:
                user = user_type()
                async def send(res):
                    await websocket.send(jsonString(user.prepare_result(res)))
                    await asyncio.sleep(1)
                user.send = send 
                user.load()
                users[address] = user
                await websocket.send(jsonString([user.menu,user.screen])) 

            async for message in websocket:                     
                if address in users:
                    user = users[address]
                else:
                    print('Unknown user search error!')
                    return
                data = json.loads(message)            
                result = user.result4message(data)
                if result:                
                    await websocket.send(jsonString(user.prepare_result(result)))
        except Exception as e:
            print('Session exception!')
            print(e,traceback.format_exc())              
        finally:        
            if address in users:
                del users[address]    
    """    
    http_handlers.insert(0, web.get('/ws', websocket_handler))
    if UniHandler.fix_file:
        http_handlers.append(web.get(UniHandler.fix_file, static_serve))
    http_handlers.append(web.get('/', static_serve))
    http_handlers.append(web.static('/js', f"{utils.webpath}/js"))
    http_handlers.append(web.static('/fonts', f"{utils.webpath}/fonts"))
    http_handlers.append(web.static('/css', f"{utils.webpath}/css"))
    http_handlers.append(web.static(f'/{upload_dir}', f"/{utils.app_user_dir}/{upload_dir}"))
    


    print(f'Start {appname} server on {port} port..')    

    app = web.Application()
    
    app.add_routes(http_handlers)
    
    web.run_app(app,  port=port)
    
