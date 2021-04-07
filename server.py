import websockets
import asyncio
import traceback
import inspect
from . import utils

from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import os
import io
import cgi
from .manager import * 

class ReqHandler(SimpleHTTPRequestHandler):    
    def log_message(self, format, *args):
        return

    def translate_path(self, path):        
        return utils.translate_path(path)

    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)    
        
    def do_POST(self):        
        r, info = self.deal_post_data()
        print(r, info, "by: ", self.client_address)
        f = io.BytesIO()
        if r:
            f.write(b"Success\n")
        else:
            f.write(b"Failed\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", str(length))        
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()      

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

def start_server(path, port=8000):
    '''Start a resource webserver serving path on port'''    
    httpd = HTTPServer(('', port), ReqHandler)    
    httpd.serve_forever()                

def start(appname, port = 8000, user_type = User, user_dir = '',pretty_print = False, 
        socket_port = 1234, upload_dir = 'upload', translate_path = None):
    set_utils(appname,user_dir,port,upload_dir, translate_path)    
    
    pretty_print = pretty_print

    daemon = threading.Thread(name='daemon_server', target=start_server, args=('.', port))
    daemon.setDaemon(True)
    daemon.start()

    indent = 4 if pretty_print else None
    
    def jsonString(obj):
        return toJson(obj, indent, pretty_print)

    async def session(websocket, path):
        address = websocket.remote_address
        try:            
            if address in users:
                user = users[address]
            else:
                user = user_type()
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
            if getattr(e,'code',0) != 1006: #client interruption
                print(e,traceback.format_exc())              
        finally:        
            if address in users:
                del users[address]    

    print(f'Start {appname} server on {port} port..')
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(session, '0.0.0.0', socket_port))
    
    while True:
        try:
            asyncio.get_event_loop().run_forever()
        except:
            print('Async core reloaded!')

