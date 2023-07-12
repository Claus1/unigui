from . import utils

class Gui:
    def __init__(self, *args, **kwargs):
        self.name = args[0]
        la = len(args)
        if la > 1:
            self.value = args[1]
        if la > 2:
            self.changed = args[2]
        for key in kwargs.keys():            
            self.add(key, kwargs[key]) 
        
    def add(self, attr, value):
        setattr(self, attr, value) 

    def check(self,*attr_names):
        for name in attr_names:
            if not hasattr(self,name):
                raise AttributeError(name, self)

    def mutate(self, obj):
        self.__dict__ = obj.__dict__    

    def accept(self, value):
        if hasattr(self, 'changed'):
            self.changed(self, value)
        else:
            self.value = value

Line = Gui("Line", type = 'line')

def smart_complete(lst, min_input_length = 2, max_output_length = 10):
    di = {it: it.lower() for it in lst}
    def complete(gui, ustr):
        if len(ustr) < min_input_length:
            return []
        ustr = ustr.lower()
        arr = [(itlow.find(ustr), it) for it, itlow in di.items() if itlow.find(ustr) != -1]
        arr.sort(key=lambda e: e[0])
        if len(arr) > max_output_length:
            arr = arr[: max_output_length]
        return [e[1] for e in arr]
    return complete

class Edit(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        if 'type' not in kwargs:
            self.type =  'autoedit' if 'complete' in kwargs else 'edit'
        self.check('value')

class Text(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = ''
        self.edit = False

class Button(Gui):
    def __init__(self, *args, **kwargs):
        self.name = args[0]
        if len(args) > 1:
            self.changed = args[1]        
        for key in kwargs.keys():            
            self.add(key, kwargs[key])

def CameraButton(name, *args,**kwargs):
    kwargs['type'] = 'camera'
    return Button(name, *args, **kwargs)

def UploadButton(name, handler,**kwargs):
    if 'type' not in kwargs:
        kwargs['type'] = 'gallery'
    if 'width' not in kwargs:
        kwargs['width'] = 250.0              
    if 'height' not in kwargs:
        kwargs['height'] = 300.0                  
    return Button(name, handler, **kwargs)

def UploadImageButton(name, handler,**kwargs):
    kwargs['type'] = 'gimages'
    return UploadButton(name, handler, **kwargs)    
        
class Image(Gui):
    '''has to contain file parameter as name'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type='image'
        if not hasattr(self,'width'):
            self.width = 500.0              
        if not hasattr(self,'image'):
            self.image = self.value if hasattr(self, 'value') else None

class Video(Gui):
    '''has to contain src parameter'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type='video'
        if not hasattr(self,'width'):
            self.width = 500.0              
        if not hasattr(self,'src'):
            raise "No video src reference!"
        if not hasattr(self,'ratio'):
            self.ratio = "9/9"

graph_default_value = {'nodes' : [], 'edges' : []}

class Graph(Gui):
    '''has to contain nodes, edges, see Readme'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type='graph'
        if not hasattr(self,'value'):
            self.value = graph_default_value
        if not hasattr(self,'minwidth'):
            self.minwidth = 600.0              
        if not hasattr(self,'minheight'):
            self.minheight = 600.0              
        self.check('nodes', 'edges')

class Switch(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check('value')        

list_types = ['toggles','list','dropdown']

class Select(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self,'options'):             
            self.options = []
        if not hasattr(self,'value'):
            self.value = None

class Tree(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)         
        self.type = 'tree' 
        if not hasattr(self,'options'):
            self.options = {}        
        if not hasattr(self,'value'):
            self.value = None

def accept_cell_value(table, val):    
    value, position = val
    if not isinstance(value, bool):
        try:
            value = float(value)        
        except ValueError:
            pass
        table.rows[position[0]][position[1]] = value    

def delete_table_row(table, value):
    if table.rows:        
        keyed = len(table.headers) < len(table.rows[0])
        table.value = value   
        if isinstance(value, list):        
            if keyed:
                table.rows = [row for row in table.rows if row[-1] not in value]
            else:
                value.sort(reverse=True)
                for v in value:            
                    del table.rows[v]
            table.value = []
        else:
            if keyed:            
                table.rows = [row for row in table.rows if row[-1] != value]
            else:
                del table.rows[value]  
            table.value = None    

def append_table_row(table, value):
    ''' append has to return new row or error string, val is search string in the table'''
    new_id_row, search = value #new_id_row == rows count
    new_row = [''] * len(table.headers)
    if search:
        new_row[0] = search
    table.rows.append(new_row)
    return new_row

class Table(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)             
        self.check('headers')
        if not hasattr(self,'type'):
            self.type = 'table'
        if not hasattr(self,'value'):
            self.value = None
        if not hasattr(self,'rows'):
            self.rows = []
        if not hasattr(self,'value'):
            self.value = None

        if getattr(self,'edit', True):
            edit_setting = hasattr(self,'modify') or hasattr(self,'delete') or hasattr(self,'append')
            if not edit_setting:                             
                self.delete = delete_table_row             
                self.append = append_table_row 
            if not hasattr(self,'modify'): 
                self.modify = accept_cell_value             
        
    def selected_list(self):                            
        return [self.value] if self.value != None else [] if type(self.value) == int else self.value   

    def clean(self):
        self.rows = []
        self.value = [] if isinstance(self.value,(tuple, list)) else None
        return self
        
class Block(Gui):
    def __init__(self, *args, **kwargs):        
        self.name = args[0]        
        self.type = 'block'
        self.value = list(args[1:])
        for key in kwargs.keys():            
            self.add(key, kwargs[key])        
        self.check()

    def check(self):
        ch_names = set()        
        for child in utils.flatten(self.value):            
            if child.name in ch_names:                        
                raise Exception(f'Error: the block {self.name} contains a duplicated name {child.name}!')                        
            ch_names.add(child.name)            

class Dialog:  
    def __init__(self, name, callback, *content, buttons = ['Ok', 'Cancel'], icon = 'not_listed_location'):
        self.name = name
        self.callback = callback  
        self.type = 'dialog'         
        self.buttons = buttons
        
        self.content = Block(name,[], *content, dialog = True, icon = icon) 

class TextViewer(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'docviewer' 
                     
class Screen(Gui):
    def __init__(self, *args, **kwargs):
        self.name = args[0]        
        for key in kwargs.keys():            
            self.add(key, kwargs[key])   
        self.type = 'screen'

    def check(self):
        bl_names = set()        
        for bl in utils.flatten(self.blocks):                                    
            if bl.name in bl_names:
                raise Exception(f'Error: the screen {self.name} contains a duplicated name {bl.name}!')                
            bl_names.add(bl.name)
            bl.check()    