import os
import importlib
import pickle
from .utils import *
from . import utils
import itertools
from datetime import datetime
import time
from .guielements import *
import sys
from . import userset

users = {}
modules = {}

sing2method = {'=' : 'changed', '->': 'update','?': 'complete','+': 'append','-':'delete', '!': 'editing', '#': 'modify','$': 'params'}        

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

        self.tool_buttons = [Button('_Back', icon='arrow_back',changed=self.go_back), 
            Button('_Forward', icon='arrow_forward',changed=self.go_forward),
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

        for file in os.listdir(screens_dir):
            if file.endswith(".py") and file != '__init__.py':
                name = file[0:-3]

                if name not in modules:                    
                    path = f'{screens_dir}/{file}'                
                    spec = importlib.util.spec_from_file_location(name,path)
                    module = importlib.util.module_from_spec(spec)
                    modules[name] = module, spec
                else:
                    module, spec = modules[name]
                
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
                        tooltip = 'Save model to disk',changed = screen.save)]
                                
                screen.check()                         
                #del sys.modules[name]       
        
        self.screens.sort(key=lambda s: s.order)
        self.screen_module = self.screens[0]
        self.menu = [[s.name,s.icon] for s in self.screens]        

        #remove user modules
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
            if (data[0] == 'root' and data[1] is None):
                self.active_dialog = None
                return                    
            elif len(data) == 2: #button pressed
                result = dialog.callback(dialog, data[1]) #data[1] == returned value
                self.active_dialog = None 
                if result is None:
                    result = self.process(data) # rise up                   
            else:
                el = self.find_element(data)
                if el:
                    result = self.process_element(el, data)                
        else:
            result = self.process(data)           

        if result and isinstance(result, Dialog):
            self.active_dialog = result
        return result

    @property
    def blocks(self):
        return [self.active_dialog.content] if self.active_dialog and self.active_dialog.content else self.screen.blocks

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
            if hasattr(raw,'prepare'):
                raw.prepare()
        else:
            if type(raw) == dict and 'update' in raw:
                raw['update'] = self.find_path(raw['data'])
            elif isinstance(raw,Gui):
                raw = {'update': self.find_path(raw), 'data': raw}
            elif isinstance(raw, list) and all(isinstance(e,Gui) for e in raw):
                raw = {'update': [self.find_path(e) for e in raw],'multi': True, 'data': raw}
        return raw

    def process(self,arr):
        if arr[0] == 'root':
            for s in self.screens:
                if s.name == arr[1]:
                    self.screen_module = s
                    if hasattr(s.screen,'prepare'):
                        s.screen.prepare()
                    return True
            return Error(f'Unknown menu {s.name}')
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
            
            if hasattr(elem, smeth):
                handler = getattr(elem, smeth)                                
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

    

