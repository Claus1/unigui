import os 
import jsonpickle
import json

resource_port = None
appname = 'Unigui'
app_user_dir = os.getcwd()
upload_dir = 'upload'
socket_ip = ''
socket_port = 1234
blocks_dir = 'blocks'        
screens_dir =  'screens'        

libpath = os.path.dirname(os.path.realpath(__file__))
webpath = libpath + '/web' 

def toJson(obj, indent, pretty_print):
    return json.dumps(json.loads(jsonpickle.encode(obj,unpicklable=False)), 
        indent = indent, sort_keys = pretty_print)

def fn2url(fn):   
    if fn[0] == '/':
        fn = fn[len(app_user_dir):]   
    s =  fn #f":{resource_port}/{fn}"
    return s.replace(' ','%20')

def url2fn(url):
    return url[url.find('/') + 1:].replace('%20',' ')

def upload_fn(fn):
    return f'{upload_dir}/{fn}'     
    
def translate_http_path(path):
    if '?' in path:
        path = path.split('?')[0]
    if path.startswith(f'/{upload_dir}/'):             
        return f'{app_user_dir}{path}'.replace('%20',' ')     
    return f'{webpath}{path}'.replace('%20',' ') 

translate_path = translate_http_path

def set_utils(appname_,port_,upload_dir_, translate_path_, socket_ip_, socket_port_):
    global appname, resource_port, upload_dir, translate_path, socket_ip, socket_port
    appname = appname_
    resource_port = port_
    upload_dir = upload_dir_
    socket_ip = socket_ip_
    socket_port = socket_port_

    if translate_path_:
        translate_path = translate_path_

def flatten(*arr):
    for a in arr:
        if isinstance(a, list):
            yield from flatten(*a)
        else:
            yield a
            
#for registering screen handlers of outer blocks
handlers__ = {}

def clean_handlers():
    global handlers__
    handlers__ = {}

def handle(elem, event):
    def h(fn):
        handlers__[elem, event] = fn
    return h

def Answer(data, param, id):
    return {'answer': data,'param': param, 'id' : id}

def Error(message, *data):
    d = {'error':message}
    if data:
        d['data'] = data
        d['update'] = None
    return d

def Info(message, *data):
    d = {'info':message}
    if data:
        d['data'] = data
        d['update'] = None
    return d
    
def Warning(message, *data):
    d = {'warning':message}
    if data:
        d['data'] = data
        d['update'] = None
    return d    

def Update(data):
    return {'data': data,'update': None}

def upload_path(fpath):
    return f'{os.getcwd()}/{upload_dir}/{fpath}'

UpdateScreen = True

