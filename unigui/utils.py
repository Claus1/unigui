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
UpdateScreen = True

libpath = os.path.dirname(os.path.realpath(__file__))
webpath = libpath + '/web' 

try:
    import config
except:
    with open('config.py', 'w') as f:        
        f.write("""port = 8000 
#for remote server socket_ip is its ip 
socket_ip = 'localhost' 
upload_dir = 'web'
pretty_print = True
hot_reload = True
""")
        print("Config with default parameters is created!")

def toJson(obj, indent, pretty_print):
    return json.dumps(json.loads(jsonpickle.encode(obj,unpicklable=False)), 
        indent = indent, sort_keys = pretty_print)

def fn2url(fn):   
    if fn[0] == '/':
        fn = fn[len(app_user_dir):]   
    return fn.replace(' ','%20')

def url2fn(url):
    return url[url.find('/') + 1:].replace('%20',' ')

def upload_fn(fn):
    return f'{upload_dir}/{fn}'     

def upload_path(fpath):
    return f'{os.getcwd()}/{upload_dir}/{fpath}'
    
def translate_http_path(path):
    if '?' in path:
        path = path.split('?')[0]
    if path.startswith(f'/{upload_dir}/'):             
        return f'{app_user_dir}{path}'.replace('%20',' ')     
    return f'{webpath}{path}'.replace('%20',' ') 

def set_utils(appname_,port_,upload_dir_, socket_ip_):
    global appname, resource_port, upload_dir, socket_ip, socket_port
    appname = appname_
    resource_port = port_
    upload_dir = upload_dir_
    socket_ip = socket_ip_
    socket_port = port_    

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

class Message:
    def __init__(self, *gui_objects, user = None):
        if gui_objects:
            self.updates = [{'data': gui} for gui in gui_objects]
            if user:
                self.fill_paths4(user)

    def fill_paths4(self, user):
        if hasattr(self, 'updates'):
            for update in self.updates:
                update['path'] = user.find_path(update['data'])

def TextMessage(type, text, *data, user = None):
    message = Message(*data, user=user)
    message.type = type
    message.value = text    
    return message    

def Warning(text, *data):
    return TextMessage('warning', text, *data)

def Error(text, *data):
    return TextMessage('error', text, *data)
    
def Info(text, *data):
    return TextMessage('info', text, *data)

def Answer(data, param, id):
    return {'type' : 'answer', 'value': data,'param': param, 'id' : id}


