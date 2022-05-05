import os
import importlib
from .utils import *
from . import utils
import itertools
import time
from .guielements import *
import sys
from . import userset
import asyncio
import requests
from threading import Thread

users = {}

sing2method = {'=':'changed', '->':'update','?':'complete','+':'append', '-':'delete', '!':'editing', '#':'modify'}    

#loop and thread for progress functionality
loop = asyncio.new_event_loop()
def f(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever() 

t = Thread(target=f, args=(loop,))
t.start()  

class User:      
    def __init__(self):   
        self.change_buffer = []
        self.redo_buffer = []      
       
        self.screens = []        
        self.active_dialog = None
        self.screen_module = None
        self.history_switching = []
        self.history_pointer = 0        

        self.oper_count = 0
        self.time_last_change = time.time()
        self.max_oper_time = 0.1  

        self.tool_buttons = [Button('_Back', icon='arrow_back',changed=self.go_back, tooltip = 'Go back'), 
            Button('_Forward', icon='arrow_forward',changed=self.go_forward, tooltip = 'Go forward'),
            Button('_Undo', icon='undo', tooltip = 'Undo last operation',changed = self.undo_last_operation),
            Button('_Redo', icon='redo', tooltip = 'Redo last operation',changed = self.redo_last_operation)]

    def append_change(self, change):
        self.change_buffer.append(change)
        curr_time = time.time()
        if curr_time - self.time_last_change > self.max_oper_time:
            self.oper_count += 1
            self.redo_buffer = [] #clean redo if new operation
        change.oper = self.oper_count
        self.time_last_change = curr_time        

    def save_changes(self,*_):
        pass

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
        for file in os.listdir(dir):
            fn = f'{dir}/{file}'
            if file[0].isdigit() and file.endswith(".js") and os.path.getsize(fn) > 25000:
                User.fix_file = f'/js/{file}'
                with open(fn, 'rb') as main:
                    b = main.read()
                    if utils.socket_ip != 'localhost':
                        b = b.replace(bytes('localhost',encoding='utf8'), bytes(str(utils.socket_ip),encoding='utf8'))                
                    if utils.resource_port != 8000:
                        b = b.replace(bytes('8000',encoding='utf8'), bytes(str(utils.resource_port),encoding='utf8'))                
                    if utils.socket_port != 1234:
                        b = b.replace(bytes('1234',encoding='utf8'), bytes(str(utils.socket_port),encoding='utf8'))                
                    User.fixed_main = b.decode("utf-8") 
                    print(f"Fixed {file} created on ip {utils.socket_ip}, http port {utils.resource_port}, socket port {utils.socket_port}.")
                    break

    def progress(self, str, *updates):
        """open or update progress window if str != null else close it  """     
        d = {'progress': str}
        if updates:
            d['update'] = None            
            d['data'] = updates         
        
        asyncio.run_coroutine_threadsafe(self.send(d), loop)
        """  loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop) # <----
        #f  = asyncio.ensure_future(self.send(d))
        loop.run_until_complete(self.send(d))    """     
                          
    def undo_last_operation(self, *_):
        if self.undo_last_changes():            
            return True  
        return Error("Nothing to undo!")
        
    def redo_last_operation(self, *_):    
        if self.redo_last_changes():            
            return True     
        return Error("Nothing to redo!")

    def redo_last_changes(self):
        if self.redo_buffer != []:
            oper = self.redo_buffer[-1].oper                
            undo_buffer_size = len(self.change_buffer)            
            return True

    def undo_last_changes(self):
        if self.change_buffer != []:
            oper = self.change_buffer[-1].oper
            redo_buffer_size = len(self.redo_buffer)            
            return True        

    def dispatch(self, elem, ref):        
        return Warning(f'What to do with {ref}?')        

    def go_back(self, *_):        
        if self.history_pointer > 0:
            self.history_pointer -= 1
            return self.dispatch(self.history_switching[self.history_pointer])
        return Info('No more back references!')

    def go_forward(self, *_):
        if self.history_pointer < len(self.history_switching) - 1:
            self.history_pointer += 1
            return self.dispatch(self.history_switching[self.history_pointer])
        return Info('No more forward references!')

    def load(self):   
        screen_vars = {
            'icon' : 'article',
            'prepare' : None,
            'dispatch' : None,
            'blocks' : [],
            'header' : utils.appname,            
            'save' : self.save_changes,
            'toolbar' : None
        }     

        userset.user = self    
        blocks_dir = 'blocks'        
        screens_dir =  'screens'
        modules = {}
        for file in os.listdir(screens_dir):
            if file.endswith(".py") and file != '__init__.py':
                name = file[0:-3]

                #if name not in modules:                    
                path = f'{screens_dir}/{file}'                
                spec = importlib.util.spec_from_file_location(name,path)
                module = importlib.util.module_from_spec(spec)
                modules[name] = module, spec
                #else:
                #    module, spec = modules[name]
                
                utils.clean_handlers()
                spec.loader.exec_module(module)            
                
                screen = Screen(module.name)
                module.screen = screen                
                self.screens.append(module)
                #set system vars
                for var in screen_vars:                                            
                    setattr(screen, var, getattr(module,var,screen_vars[var])) 
                screen.handlers__ = utils.handlers__
                
                if not screen.toolbar:
                    screen.toolbar = [*self.tool_buttons, Button('_Save model', icon='cloud_upload', 
                        tooltip = 'Save to disk',changed = screen.save)]
                                
                screen.check()                         
                #del sys.modules[name]       
        
        self.screens.sort(key=lambda s: s.order)
        main = self.screens[0]
        if 'prepare' in dir(main):
            main.prepare()
        self.screen_module = main
        self.menu = [[s.name,s.icon] for s in self.screens]        

        #remove user modules from sys for repeating loading for new users
        for file in os.listdir(blocks_dir):
            if file.endswith(".py") and file != '__init__.py':
                name = f'{blocks_dir}.{file[0:-3]}'
                if name in sys.modules:
                    del sys.modules[name]       
                
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
                result = dialog.callback(dialog, data[1]) #data[1] == returned value                                
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
                for c in itertools.chain(bl.top_childs, bl.childs):
                    if type(c) == list:
                        for sub in c:
                            if sub.name == path[1]:
                                return sub
                    elif c.name == path[1]:
                        return c

    def find_path(self, elem):        
        for bl in flatten(self.blocks):        
            if bl == elem:
                return [bl.name]
            for c in itertools.chain(bl.top_childs, bl.childs):
                if type(c) == list:
                    for sub in c:
                        if sub == elem:
                            return [bl.name, sub.name]
                elif c == elem:
                    return [bl.name, c.name]

    def prepare_result(self, raw):
        if raw == UpdateScreen:
            raw = self.screen            
            #if getattr(raw,'prepare', False):
            #    raw.prepare()
        else:
            if type(raw) == dict and 'update' in raw:
                if isinstance(raw['data'], (list,tuple)):
                    raw['multi'] = True
                    raw['update'] = [self.find_path(e) for e in raw['data']]
                else:
                    raw['update'] = self.find_path(raw['data'])
            elif isinstance(raw,Gui):
                 raw = {'update': self.find_path(raw), 'data': raw}
            elif isinstance(raw, (list, tuple)) and all(isinstance(e,Gui) for e in raw):
                raw = {'update': [self.find_path(e) for e in raw],'multi': True, 'data': raw}
        return raw

    def process(self,arr):
        if arr[0] == 'root':
            for s in self.screens:
                if s.name == arr[1]:
                    self.screen_module = s
                    if getattr(s.screen,'prepare', False):
                        s.screen.prepare()
                    return True            
            print(f'Unknown root command {s.name}')
            return 
        elem = self.find_element(arr)
        #recursive for Signals
        while True:
            res = self.process_element(elem, arr)
            if not isinstance(res, Signal):
                return res
            elem = res.elem
            arr = res.arr                            
        
    def process_element(self, elem, arr):        
        id = arr.pop() if len(arr) == 5 else 0
        sign = arr[-2]
        smeth = sing2method.get(sign)
        val = arr[-1]
        if smeth:
            handler = self.screen.handlers__.get((elem, smeth))
            if handler:
                result = handler(elem, val)                
                return result
            
            handler = getattr(elem, smeth, False)                                
            if handler:                
                res = handler(elem, val)  
                if id:                        
                    res = Answer(res, None, id)                
                return res
            elif sign == '=':
                if hasattr(elem,'value'): #exlude Buttons and others without 'value'
                    elem.value = val                                        
                return                
            elif sign == '$': #update element params
                for param in val:
                    setattr(elem, param, val[param])                                        
                return                

        elif sign == '@': #reference
            result = False            
            if hasattr(elem, 'dispatch'):
                result = elem.dispatch(elem, val)
            else:
                scr = self.screen
                for bl in flatten(self.blocks):        
                    if hasattr(bl, 'dispatch') and elem in flatten(bl.childs, bl.top_childs):
                        result = bl.dispatch(elem, val) 
                        break
                else:
                    if scr.dispatch:
                        result = scr.dispatch(elem, val) 
                    else:    
                        result = self.dispatch(elem, val) 
            if result is not None:
                return result        

        if sign != '!': #editing can omit
            return Error(f'{elem} does not contain method for {sign} event type!')

    

