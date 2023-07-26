import os, jsonpickle, json, platform, requests

blocks_dir = 'blocks'        
screens_dir =  'screens'        
UpdateScreen = True

divpath = '\\' if platform.system() == 'Windows' else '/'
libpath = os.path.dirname(os.path.realpath(__file__))
webpath = f'{libpath}{divpath}web' 
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

def toJson(obj, indent, pretty):
    js = jsonpickle.encode(obj,unpicklable=False)
    return json.dumps(json.loads(js), indent=indent, sort_keys=pretty) if pretty else js

def filename2url(fn):   
    if fn[0] == '/' or fn[1] == ':': #if full path
        fn = fn[len(app_dir):]   
    return fn.replace(' ','%20')

def url2filepath(url):
    return url[url.find('/') + 1:].replace('%20',' ')   

def url2filename(url):
    return url[url.rfind('/') + 1:].replace('%20',' ')   

def upload_path(fpath):
    return f'{config.upload_dir}{divpath}{fpath}'

def flatten(*arr):
    for a in arr:
        if isinstance(a, list):
            yield from flatten(*a)
        else:
            yield a
    
def cache_url(url):
    """cache url file in upload_dir and returns the local file name"""
    fname = url2filename(url)   
    fname = upload_path(fname)
    response = requests.get(url)
    if response.status_code != 200:
        return None
    file = open(fname, "wb")
    file.write(response.content)
    file.close() 
    return fname

class Message:
    def __init__(self, *gui_objects, user = None):        
        self.updates = [{'data': gui} for gui in gui_objects] if gui_objects else []
        if user:
            self.fill_paths4(user)

    def fill_paths4(self, user):
        if hasattr(self, 'updates'):
            for update in self.updates:
                update['path'] = user.find_path(update['data'])

    def contains(self, guiobj):
        for update in self.updates:
            if guiobj is update['data']:
                return True

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


