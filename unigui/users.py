import importlib
from .utils import *
from .guielements import *
from .common import *
from .containers import Dialog, Screen
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
        self.last_message = None              
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
        if not self.testing:           
            self.sync_send(TypeMessage('progress', str, *updates, user = self))
                   
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
        return self.process(ArgObject(block = 'root', element = None, value = name))

    def result4message(self, message):
        result = None
        dialog = self.active_dialog
        if dialog:            
            if message.element is None: #button pressed
                self.active_dialog = None                
                result = dialog.changed(dialog, message.value) 
            else:
                el = self.find_element(message)
                if el:
                    result = self.process_element(el, message)                        
        else:
            result = self.process(message)           
        if result and isinstance(result, Dialog):
            self.active_dialog = result
        return result

    @property
    def blocks(self):
        return [self.active_dialog] if self.active_dialog and \
            self.active_dialog.value else self.screen.blocks

    def find_element(self, message):               
        blname = message.block
        elname = message.element
        if blname == 'toolbar':
            for e in self.screen.toolbar:
                if e.name == elname:                
                    return e
        else:
            for bl in flatten(self.blocks):
                if bl.name == blname:
                    for c in bl.value:
                        if isinstance(c, list):
                            for sub in c:
                                if sub.name == elname:
                                    return sub
                        elif c.name == elname:
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

    def process(self, message):
        self.last_message = message     
        screen_change_message = message.screen and self.screen.name != message.screen   
        if is_screen_switch(message) or screen_change_message:
            for s in self.screens:
                if s.name == message.value:
                    self.screen_module = s                    
                    if screen_change_message:
                        break
                    if getattr(s.screen,'prepare', False):
                        s.screen.prepare()
                    return True 
            else:        
                error = f'Unknown screen name: {message.value}'   
                self.log(error)
                return Error(error)
        
        elem = self.find_element(message)          
        if elem:                          
            return self.process_element(elem, message)  
        
        error = f'Element {message.block}>>{message.element} does not exists!'
        self.log(error)
        return Error(error)
        
    def process_element(self, elem, message):                
        event = message.event        
        query = event in ['complete', 'append']
        
        handler = self.__handlers__.get((elem, event), None)
        if handler:
            result = handler(elem, message.value)                
            return result
        
        handler = getattr(elem, event, False)                                
        if handler:                
            result = handler(elem, message.value)  
            if query:                        
                result = Answer(event, message, result)                
            return result
        elif event == 'changed':            
            elem.value = message.value                                        
        else:
            self.log(f'{elem} does not contain method for {event} event type!')                     
            return Error(f'Invalid {event} event type for {message.block}>>{message.element} is received!')

    def reflect(self):        
        user = User.UserType()
        user.screens = self.screens
        if self.screens:
            user.screen_module = self.screens[0]     
        user.__handlers__ =  self.__handlers__        
        return user

    def log(self, str, type = 'error'):        
        scr = self.screen.name if self.screens else 'omitted'
        str = f"session: {self.session}, screen: {scr}, message: {self.last_message} \n  {str}"
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
