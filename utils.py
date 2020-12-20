import os 

resource_port = 1235
appname = 'Unigui'
app_user_dir = ''
upload_dir = 'upload'

libpath = os.path.dirname(os.path.realpath(__file__))
webpath = libpath + '/web' 

def translate_http_path(path):
    if path == '/':
        path = '/index.html'
    return f'{webpath}{path}'.replace('%20',' ') 

translate_path = translate_http_path

def flutten(*arr):
    for a in arr:
        if isinstance(a, list):
            yield from flutten(*a)
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