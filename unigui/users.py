import importlib
from .utils import *
from .guielements import *
from .blocks import Dialog, Screen
import sys
import asyncio
from threading import Thread
import logging

class User:      
    def __init__(self):          
        self.screens = []        
        self.active_dialog = None
        self.screen_module = None 
        self.session = None   
        self.__handlers__ = {}                    
        User.last_user = self   

    async def send_windows(self, obj):  
        await self.send(obj)        
        self.transport._write_fut = None
        self.transport._loop._ready.pop()

    def sync_send(self, obj):                    
        asyncio.run_coroutine_threadsafe(self.send_windows(obj) 
            if self.transport else self.send(obj), self.extra_loop)

    def progress(self, str, *updates):
        """open or update progress window if str != null else close it  """             
        return self.sync_send(TypeMessage('progress', str, *updates, user = self))
                   
    def load_screen(self, file):
        screen_vars = {
            'icon' : None,
            'prepare' : None,            
            'blocks' : [],
            'header' : config.appname,                        
            'toolbar' : [], 
            'order' : 0,
            'reload': config.hot_reload 
        }             
        name = file[:-3]        
        path = f'{screens_dir}{divpath}{file}'                
        spec = importlib.util.spec_from_file_location(name,path)
        module = importlib.util.module_from_spec(spec)        
                
        module.user = self                               
        
        spec.loader.exec_module(module)            
        screen = Screen(getattr(module, 'name', ''))
        #set system vars
        for var in screen_vars:                                            
            setattr(screen, var, getattr(module,var,screen_vars[var]))         
        
        if screen.toolbar:
            screen.toolbar += User.toolbar
        else: 
            screen.toolbar = User.toolbar  
                                
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
                    module = self.load_screen(file)                
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
        menu = [[getattr(s, 'name', ''),getattr(s,'icon', None)] for s in self.screens]        
        for s in self.screens:
            s.screen.menu = menu

    @property
    def testing(self):        
        return  self.session == 'autotest'
    
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
        blname = path[0]
        elname = path[1]
        for bl in flatten(self.blocks):
            if bl.name == blname:
                for c in bl.value:
                    if isinstance(c, list):
                        for sub in c:
                            if sub.name == elname:
                                return sub
                    elif c.name == elname:
                        return c
        if blname == 'toolbar':
            for e in self.screen.toolbar:
                if e.name == elname:                
                    return e

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
        for e in self.screen.toolbar:
            if e == elem:                
                return ['toolbar', e.name]

    def prepare_result(self, raw):
        if raw == UpdateScreen:
            raw = self.screen      
            raw.reload = False                  
        elif raw == Redesign:
            raw = self.screen      
            raw.reload = True                  
        else:
            if isinstance(raw, Message):
                raw.fill_paths4(self)                
            elif isinstance(raw,Gui):
                raw = Message(raw, user = self)                 
            elif isinstance(raw, (list, tuple)):
                raw = Message(*raw, user = self)
        return raw

    def process(self,arr):
        self.last_input = arr        
        if arr[0] == 'root':
            for s in self.screens:
                if s.name == arr[1]:
                    self.screen_module = s
                    if getattr(s.screen,'prepare', False):
                        s.screen.prepare()
                    return True            
            self.log(f'Unknown screen name: {s.name}')
        else:
            elem = self.find_element(arr)                                    
            return self.process_element(elem, arr) if elem else \
                Error(f'Element {arr[0]}>>{arr[1]} does not exists!')       
        
    def process_element(self, elem, arr):                
        action = arr[-2]        
        val = arr[-1]
        query = action in ['complete', 'append']
        
        handler = self.__handlers__.get((elem, action), None)
        if handler:
            result = handler(elem, val)                
            return result
        
        handler = getattr(elem, action, False)                                
        if handler:                
            result = handler(elem, val)  
            if query:                        
                result = Answer(action, arr[:2], result)                
            return result
        elif action == 'changed':            
            elem.value = val                                        
        else:
            self.log(f'{elem} does not contain method for {action} event type!')                     
            return Error(f'Invalid {action} event type for {arr[0]}>>{arr[1]} element is received!')

    def reflect(self):        
        user = User.UserType()
        user.screens = self.screens
        if self.screens:
            user.screen_module = self.screens[0]     
        user.__handlers__ =  self.__handlers__        
        return user

    def log(self, str, type = 'error'):        
        scr = self.screen.name if self.screens else 'omitted'
        str = f"session: {self.session}, screen: {scr}, message: {self.last_input} \n  {str}"
        if type == 'error':
            logging.error(str)
        else:
            logging.warning(str)    

def make_user():
    if config.mirror and User.last_user:
        user = User.last_user.reflect()
        ok = user.screens
    else:
        user = User.UserType()
        ok = user.load()
    if config.mirror:
        User.reflections.append(user)         
    return user, ok

#loop and thread is for progress window and sync interactions
loop = asyncio.new_event_loop()

def f(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever() 

async_thread = Thread(target=f, args=(loop,))
async_thread.start()

def handle(elem, event):
    def h(fn):
        User.last_user.__handlers__[elem, event] = fn
    return h

User.extra_loop = loop
User.UserType = User
User.last_user = None
User.toolbar = []
User.reflections = []
