import os, jsonpickle, json, platform, requests

blocks_dir = 'blocks'        
screens_dir =  'screens'        
UpdateScreen = True
Redesign = 2
public_dirs = 'public_dirs'

divpath = '\\' if platform.system() == 'Windows' else '/'
libpath = os.path.dirname(os.path.realpath(__file__))
webpath = f'{libpath}{divpath}web' 
app_dir = os.getcwd()

try:
    import config
except:
    f = open('config.py', 'w')  
    f.write("""port = 8000 
upload_dir = 'web'
hot_reload   = True
logfile  = 'log'
autotest = '*'
appname = 'Unigui'
""")
    f.close()
    import config
    print("Config with default parameters is created!")

def toJson(obj, indent, pretty):
    js = jsonpickle.encode(obj,unpicklable=False)
    return json.dumps(json.loads(js), indent=indent, sort_keys=pretty) if pretty else js

def filename2url(fn):   
    if fn[0] == '/' or fn[1] == ':': #if full path
        fn = fn[len(app_dir):]   
    if fn[0] == divpath:
        fn = fn[1:]
    return fn 

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
        if gui_objects:
            self.updates = [{'data': gui} for gui in gui_objects]
        if user:
            self.fill_paths4(user)

    def fill_paths4(self, user):
        if hasattr(self, 'updates'):
            invalid = []
            for update in self.updates:
                data = update["data"]
                path = user.find_path(data)
                if path:
                    update['path'] = path
                else:
                    invalid.append(update)                    
                    user.log(f'Invalid element update {data.name}, type {data.type}.\n\
                    Such element not on the screen!')
            for inv in invalid:
                self.updates.remove(inv)

    def contains(self, guiobj):
        if hasattr(self, 'updates'):
            for update in self.updates:
                if guiobj is update['data']:
                    return True

def TypeMessage(type, value, *data, user = None):
    message = Message(*data, user=user)
    message.type = type
    message.value = value    
    return message    

def Warning(text, *data):
    return TypeMessage('warning', text, *data)

def Error(text, *data):
    return TypeMessage('error', text, *data)
    
def Info(text, *data):
    return TypeMessage('info', text, *data)

def Answer(type, path, result):
    ms = TypeMessage(type, result)
    ms.path = path
    return ms


