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

    def mutate(self, obj):
        self.__dict__ = obj.__dict__    

    def accept(self, value):
        if hasattr(self, 'changed'):
            self.changed(self, value)
        else:
            self.value = value

Line = Gui("Line", type = 'line')

def smart_complete(lst, min_input_length = 1, max_output_length = 10):
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
        if not hasattr(self,'value'):
            self.value = '' if self.type != 'number' else 0

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

def CameraButton(name, *args):    
    return Button(name, *args, type = 'camera')
        
def UploadImageButton(name, handler,**kwargs):    
    kwargs['type'] = 'image_uploader'
    if 'width' not in kwargs:
        kwargs['width'] = 250.0              
    if 'height' not in kwargs:
        kwargs['height'] = 300.0         
    return Button(name, handler, **kwargs)

UploadButton = UploadImageButton

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
        if not hasattr(self, 'nodes'):
            self.nodes = []
        if not hasattr(self, 'edges'):
            self.edges = []

class Switch(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self,'value'):
            self.value = False

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
        if not hasattr(self,'headers'):
            self.headers = []
        if not hasattr(self,'type'):
            self.type = 'table'
        if not hasattr(self,'value'):
            self.value = None
        if not hasattr(self,'rows'):
            self.rows = []
        if not hasattr(self,'value'):
            self.value = None
        if not hasattr(self,'dense'):
            self.dense = True

        if getattr(self,'edit', True):
            edit_setting = hasattr(self,'modify') or hasattr(self,'delete') or hasattr(self,'append')
            if not edit_setting:                             
                self.delete = delete_table_row             
                self.append = append_table_row             
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

    def check(self):
        ch_names = set()        
        for child in utils.flatten(self.value):            
            if child.name in ch_names:                        
                return f'The block {self.name} contains a duplicated element name "{child.name}"!'                        
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
                return (f'The screen {self.name} contains a duplicated block name {bl.name}!')                
            bl_names.add(bl.name)
            errstr = bl.check()    
            if errstr:
                return errstr