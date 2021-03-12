import os 
import jsonpickle
import json

resource_port = None
appname = 'Unigui'
app_user_dir = os.getcwd()
upload_dir = 'upload'

libpath = os.path.dirname(os.path.realpath(__file__))
webpath = libpath + '/web' 

def toJson(obj, indent, pretty_print):
    return json.dumps(json.loads(jsonpickle.encode(obj,unpicklable=False)), 
        indent = indent, sort_keys = pretty_print)

def fn2url(fn):      
    s =  f":{resource_port}/{fn}"
    return s.replace(' ','%20')

def url2fn(url):
    return url[url.find('/') + 1:].replace('%20',' ')
    
def translate_http_path(path):
    if '?' in path:
        path = path.split('?')[0]
    if path.startswith(f'/{upload_dir}/'):             
        return f'{app_user_dir}{path}'.replace('%20',' ')     
    return f'{webpath}{path}'.replace('%20',' ') 

translate_path = translate_http_path

def set_utils(appname_,user_dir_,port_,upload_dir_, translate_path_):
    global appname, resource_port, upload_dir, translate_path
    appname = appname_
    resource_port = port_
    upload_dir = upload_dir_
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

def Error(message):
    return {'error':message}

def Info(message):
    return {'info':message}

def Warning(message):
    return {'warning':message}

def Update(data):
    return {'data': data,'update': None}

def UpdateError(data, message):
    return {'data': data, 'error':message, 'update': None}

def upload_path(fpath):
    return f'{os.getcwd()}/{upload_dir}/{fpath}'

UpdateScreen = True

class Signal:
    def __init__(self, elem, signal):
        if not signal.startswith('@'):
            signal = f'@{signal}'
        self.arr = ('@', signal)
        self.elem = elem
