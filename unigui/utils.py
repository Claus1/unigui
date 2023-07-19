import os 
import jsonpickle
import json

blocks_dir = 'blocks'        
screens_dir =  'screens'        
UpdateScreen = True

libpath = os.path.dirname(os.path.realpath(__file__))
webpath = libpath + '/web' 
app_dir = os.getcwd()

try:
    import config
except:
    with open('config.py', 'w') as f:        
        f.write("""port = 8000 
upload_dir = 'web'
pretty_print = True
hot_reload   = True
logfile  = 'log'
autotest = '*'
""")
        import config
        print("Config with default parameters is created!")

def toJson(obj, indent, pretty_print):
    return json.dumps(json.loads(jsonpickle.encode(obj,unpicklable=False)), 
        indent = indent, sort_keys = pretty_print)

def filename2url(fn):   
    if fn[0] == '/':
        fn = fn[len(app_dir):]   
    return fn.replace(' ','%20')

def url2filename(url):
    return url[url.find('/') + 1:].replace('%20',' ')   

def upload_path(fpath):
    return f'{config.upload_dir}/{fpath}'

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


