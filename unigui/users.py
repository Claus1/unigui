import importlib
from .utils import *
from .guielements import *
import sys
import asyncio
import requests
from threading import Thread
import logging

class User:      
    def __init__(self):          
        self.screens = []        
        self.active_dialog = None
        self.screen_module = None                        
        User.last_user = self        

    def log(self, str, type = 'error'):        
        scr = self.screen.name if self.screens else 'omitted'
        str = f"session: {self.session__}, screen: {scr}, message: {self.message__} \n  {str}"
        if type == 'error':
            logging.error(str)
        else:
            logging.warning(str)

    @staticmethod
    def cache_name(url):    
        name = url.split('/')[-1]
        name = utils.upload_path(name)
        return name
        
    @staticmethod
    def cache_url(url):
        "returns cached name of url image"
        cname = User.cache_name(url)
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
        b = None        
        def replace(what, tothat):
            return b.replace(bytes(what,encoding='utf8'), bytes(str(tothat),encoding='utf8'))  
        for file in os.listdir(dir):
            fn = f'{dir}/{file}'
            if file[0].isdigit() and file.endswith(".js") and os.path.getsize(fn) > 25000:
                User.fix_file = f'/js/{file}'
                with open(fn, 'rb') as main:
                    b = main.read()
                    if utils.socket_ip != 'localhost':
                        b = replace('localhost', utils.socket_ip)
                    if utils.resource_port != 8000:
                        b = replace('8000',utils.resource_port)                    
                    User.fixed_main = b.decode("utf-8") 
                    print(f"Configuring for http port {utils.resource_port}, socket ip is {utils.socket_ip}.")
                    break

    def sync_send(self, obj):
        asyncio.run_coroutine_threadsafe(self.send(obj), self.extra_loop)            

    def progress(self, str, *updates):
        """open or update progress window if str != null else close it  """             
        return self.sync_send(TextMessage('progress', str, *updates, user = self))
                       
    def load_module(self, file):
        screen_vars = {
            'icon' : None,
            'prepare' : None,            
            'blocks' : [],
            'header' : utils.appname,                        
            'toolbar' : User.toolbar, 
            'order' : 0
        }             
        name = file[0:-3]        
        path = f'{screens_dir}/{file}'                
        spec = importlib.util.spec_from_file_location(name,path)
        module = importlib.util.module_from_spec(spec)        
        
        utils.clean_handlers()                                        
        module.user = self                               
        
        spec.loader.exec_module(module)            
        screen = Screen(module.name)
        #set system vars
        for var in screen_vars:                                            
            setattr(screen, var, getattr(module,var,screen_vars[var])) 
        module.handlers__ = utils.handlers__
        
        if screen.toolbar:
            screen.toolbar += User.toolbar
        else: 
            screen.toolbar = User.toolbar  
                        
        screen.check()                         
        module.screen = screen
        return module

    def set_clean(self):
        #remove user modules from sys 
        if os.path.exists(blocks_dir):
            for file in os.listdir(blocks_dir):
                if file.endswith(".py") and file != '__init__.py':
                    name = f'{blocks_dir}.{file[0:-3]}'
                    if name in sys.modules:
                        sys.modules[name].user = self
                        del sys.modules[name]                          
    def load(self):              
        if os.path.exists(screens_dir):
            for file in os.listdir(screens_dir):
                if file.endswith(".py") and file != '__init__.py':
                    module = self.load_module(file)                
                    self.screens.append(module)                
            
        if self.screens:
            self.screens.sort(key=lambda s: s.screen.order)            
            main = self.screens[0]
            if 'prepare' in dir(main):
                main.prepare()
            self.screen_module = main
            self.update_menu()
            self.set_clean()       
            return True                 

    def update_menu(self):
        menu = [[s.name,getattr(s,'icon', None)] for s in self.screens]        
        for s in self.screens:
            s.screen.menu = menu

    @property
    def screen(self):        
        return  self.screen_module.screen 

    def set_screen(self,name):
        return self.process(['root', name])

    def result4message(self, data):
        result = None
        dialog = self.active_dialog
        if dialog:            
            if len(data) == 2: #button pressed
                self.active_dialog = None
                #data[1] is returned value                                
                result = dialog.callback(dialog, data[1]) 
            else:
                el = self.find_element(data)
                if el:
                    result = self.process_element(el, data)                
        elif len(data) == 2 and not data[1]: #dialog closed            
            return    
        else:
            result = self.process(data)           
        if result and isinstance(result, Dialog):
            self.active_dialog = result
        return result

    @property
    def blocks(self):
        return [self.active_dialog.content] if self.active_dialog and \
            self.active_dialog.content else self.screen.blocks

    def find_element(self, path):       
        if path[0] == 'toolbar':
            for e in self.screen.toolbar:
                if e.name == path[1]:                
                    return e
        for bl in flatten(self.blocks):
            if bl.name == path[0]:
                for c in bl.value:
                    if isinstance(c, list):
                        for sub in c:
                            if sub.name == path[1]:
                                return sub
                    elif c.name == path[1]:
                        return c

    def find_path(self, elem):        
        for bl in flatten(self.blocks):        
            if bl == elem:
                return [bl.name]
            for c in bl.value:
                if isinstance(c, list):
                    for sub in c:
                        if sub == elem:
                            return [bl.name, sub.name]
                elif c == elem:
                    return [bl.name, c.name]

    def prepare_result(self, raw):
        if raw == UpdateScreen:
            raw = self.screen                        
        else:
            if isinstance(raw, Message):
                raw.fill_paths4(self)                
            elif isinstance(raw,Gui):
                raw = Message(raw, user = self)                 
            elif isinstance(raw, (list, tuple)) and all(isinstance(e,Gui) for e in raw):
                raw = Message(*raw, user = self)
        return raw

    def process(self,arr):
        self.message__ = arr        
        if arr[0] == 'root':
            for s in self.screens:
                if s.name == arr[1]:
                    self.screen_module = s
                    if getattr(s.screen,'prepare', False):
                        s.screen.prepare()
                    return True            
            print(f'Unknown screen name: {s.name}')
        else:
            elem = self.find_element(arr)                        
            return self.process_element(elem, arr)        
        
    def process_element(self, elem, arr):        
        id = arr.pop() if len(arr) == 5 else 0
        action = arr[-2]        
        val = arr[-1]
        
        handler = self.screen_module.handlers__.get((elem, action))
        if handler:
            result = handler(elem, val)                
            return result
        
        handler = getattr(elem, action, False)                                
        if handler:                
            res = handler(elem, val)  
            if id:                        
                res = Answer(res, None, id)                
            return res
        elif action == 'changed':
            if hasattr(elem,'value'): #exlude Buttons and others without 'value'
                elem.value = val                                        
            return                        

        return Error(f'{elem} does not contain method for {action} event type!')

#loop and thread is for progress window and sync interactions
loop = asyncio.new_event_loop()
User.extra_loop = loop

def f(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever() 
    
async_thread = Thread(target=f, args=(loop,))
async_thread.start()  

User.toolbar = []

#Logging 
format = "%(asctime)s - %(levelname)s - %(message)s"
handlers = [logging.FileHandler(config.logfile), logging.StreamHandler()] if hasattr(config,'logfile') else []
logging.basicConfig(level = logging.WARNING, format = format, handlers = handlers)


