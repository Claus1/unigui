import os
import importlib
import pickle
from utils import *
import utils
import itertools
from datetime import datetime
import time
from guielements import *
import sys
import userset

screens_dir = "screens"
user_dir = 'user'

users = {}

sing2method = {'=' : 'changed', '->': 'update','?': 'query','+': 'append','-':'delete', '!': 'edit_status'}    

class User:      
    def __init__(self):   
        self.selected_concept = -1        
        self.change_buffer = []
        self.redo_buffer = []      

        self.considered = {}
        self.screens = []
        self.chain = []
        self.active_dialog = None
        self.active_screen = None
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

    def dispatch(self, arr):        
        value = arr[-1]
        if arr[-2] == '@': #reference
            name = value[1:]
            #???
            return UpdateScreen

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
            'blocks' : [],
            'header' : utils.appname,
            'dispatch': None,
            'save' : self.save_changes,
            'toolbar' : None
        }     
        userset.user = self
        for file in os.listdir(screens_dir):
            if file.endswith(".py") and file != '__init__.py':
                name = f'{screens_dir}.{file[0:-3]}'
                module = importlib.import_module(name)
                screen = Screen(module.name)
                module.screen = screen                
                self.screens.append(module)
                #set system vars
                for var in screen_vars:                                            
                    setattr(screen, var, getattr(module,var,screen_vars[var])) 
                
                if not screen.toolbar:
                    screen.toolbar = [*self.tool_buttons, Button('_Save model', icon='cloud_upload', 
                        tooltip = 'Save model to disk',changed = screen.save)]
                                
                screen.check()                                  
                del sys.modules[name]       
        
        self.screens.sort(key=lambda s: s.order)
        self.active_screen = self.screens[0]
        self.menu = [[s.name,s.icon] for s in self.screens]        

        #remove user modules
        for file in os.listdir(user_dir):
            if file.endswith(".py") and file != '__init__.py':
                name = f'{user_dir}.{file[0:-3]}'
                if name in sys.modules:
                    del sys.modules[name]       
                
    @property
    def screen(self):        
        return  self.active_screen.screen 

    def set_screen(self,name):
        return self.process(['root', name])

    def result4message(self, data):
        result = None
        if self.active_dialog:
            if (data[0] == 'root' and data[1] is None):
                self.active_dialog = None
                return                    
            elif len(data) == 2: #button pressed
                result = self.active_dialog.callback(data[1]) #data[1] == returned value
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

    def find_element(self, path):
        
        blocks = [self.active_dialog.content] if self.active_dialog and self.active_dialog.content else self.screen.blocks

        if path[0] == 'toolbar':
            for e in self.screen.toolbar:
                if e.name == path[1]:                
                    return e
        for bl in blocks:
            if bl.name == path[0]:
                for c in itertools.chain(bl.top_childs, bl.childs):
                    if type(c) == list:
                        for sub in c:
                            if sub.name == path[1]:
                                return sub
                    elif c.name == path[1]:
                        return c

    def find_path(self, elem):
        
        blocks = [self.active_dialog.content] if self.active_dialog and self.active_dialog.content else self.screen.blocks

        for bl in blocks:        
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
                    self.active_screen = s
                    if hasattr(s.screen,'prepare'):
                        s.screen.prepare()
                    return True
            return Error(f'Unknown menu {s.name}')
        elem = self.find_element(arr)
        return self.process_element(elem, arr)
        
    def process_element(self, elem, arr):
        sign = arr[-2]
        if sign in sing2method.keys():
            if hasattr(elem, sing2method[sign]):
                handler = getattr(elem, sing2method[sign])                
                if sign == '?': #query
                    #query params == user, query value
                    res = Answer(handler(self, arr[-1]), arr)
                else:
                    res = handler(elem, arr[-1]) #query params == user, query value
                return res
            else:
                if sign == '=':
                    if hasattr(elem,'value'): #exlude Buttons and others without 'value'
                        elem.value = arr[-1]                    
                    if self.screen.dispatch:
                        result = self.screen.dispatch(arr)
                        if result is not None:
                            return result
                    else:
                        print(elem, arr[-2], arr[-1])
                    return
                else:
                    return Error(f'{elem} does not contains method {sing2method[sign]}')
        else:
            scr = self.screen
            for bl in scr.blocks:        
                if elem in bl.childs and 'dispatch' in dir(bl):
                    result = bl.dispatch(elem, arr[-1]) 
                    if result is not None:
                        return result
            if scr.dispatch:
                result = scr.dispatch(arr) 
                if result is not None:
                    return result

            result = self.dispatch(arr) #toolbar.dispatch
            if result is not None:
                return result

        return Error(f'{elem} does not contain method for {arr[-1]}')

first_user = User()
first_user.load()

def new_user():
    global first_user
    if first_user:
        ret_user = first_user
        first_user = None
        return ret_user
    else:
        user = User()
        user.load()
        return user

