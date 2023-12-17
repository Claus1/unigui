class Gui:
    def __init__(self, name, *args, **kwargs):
        self.name = name
        la = len(args)
        if la:
            self.value = args[0]
        if la > 1:
            self.changed = args[1]                    
        self.add(kwargs) 
        
    def add(self, kwargs):              
        for key, value in kwargs.items():
            setattr(self, key, value) 

    def mutate(self, obj):
        self.__dict__ = obj.__dict__ 
    
    def accept(self, value):
        if hasattr(self, 'changed'):
            self.changed(self, value)
        else:
            self.value = value

Line = Gui("Line", type = 'line')

def smart_complete(lst, min_input_length = 0, max_output_length = 20):
    di = {it: it.lower() for it in lst}
    def complete(gui, ustr):
        if len(ustr) < min_input_length:
            return []
        ustr = ustr.lower()
        arr = [(itlow.find(ustr), it, itlow) for it, itlow in di.items() if itlow.find(ustr) != -1]
        arr.sort(key=lambda e: (e[0], e[2]))
        if len(arr) > max_output_length:
            arr = arr[: max_output_length]
        return [e[1] for e in arr]
    return complete

class Edit(Gui):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)        
        has_value = hasattr(self,'value')
        if 'type' not in kwargs:            
            if has_value:
                type_value = type(self.value)
                if type_value == int or type_value == float:
                    self.type = 'number'
                    return
            self.type =  'autoedit' if 'complete' in kwargs else 'edit'
        if not has_value:
            self.value = '' if self.type != 'number' else 0

class Text(Gui):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.value = self.name
        self.type = 'text'        

class Range(Gui):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)    
        if not hasattr(self, 'value'):
            self.value = 1.0    
        self.type = 'range'                
        if 'options' not in kwargs:
            self.options = [self.value - 10, self.value + 10, 1]

class ContentScaler(Range):
    def __init__(self, *args, **kwargs):
        name = args[0] if args else 'Scale content'        
        super().__init__(name, *args, **kwargs)                
        if 'options' not in kwargs:
            self.options = [0.25, 3.0, 0.25]
        self.changed = self.scaler
        
    def scaler(self, _, val):
        prev = self.value
        elements = self.elements() 
        self.value = val
        if elements:
            prev /= val
            for element in elements:
                element.width /= prev
                element.height /= prev            
            return elements

class Button(Gui):
    def __init__(self, name, handler = None, **kwargs):
        self.name = name
        self.add(kwargs)
        if not hasattr(self, 'type'):
            self.type = 'button'
        if handler:
            self.changed = handler
            
def CameraButton(name, handler = None, **kwargs):    
    kwargs['type'] = 'camera'
    return Button(name, handler, **kwargs)
        
def UploadImageButton(name, handler = None,**kwargs):    
    kwargs['type'] = 'image_uploader'
    if 'width' not in kwargs:
        kwargs['width'] = 250.0                  
    return Button(name, handler, **kwargs)

UploadButton = UploadImageButton

class Image(Gui):
    '''has to contain file parameter as name'''
    def __init__(self,name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.type='image'
        if not hasattr(self,'width'):
            self.width = 500.0              
        if not hasattr(self,'url'):
            self.url = self.name
        #mask full win path from Chrome detector
        if self.url[1] == ':': 
            self.url = f'/{self.url}'

class Video(Gui):
    '''has to contain src parameter'''
    def __init__(self,name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.type = 'video'
        if not hasattr(self,'width'):
            self.width = 500.0              
        if not hasattr(self,'url'):
            self.url = self.name
        if not hasattr(self,'ratio'):
            self.ratio = None

graph_default_value = {'nodes' : [], 'edges' : []}

class Graph(Gui):
    '''has to contain nodes, edges, see Readme'''
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.type='graph'
        if not hasattr(self,'value'):
            self.value = graph_default_value
        if not hasattr(self,'minwidth'):
            self.minwidth = 600.0                      
        if not hasattr(self, 'nodes'):
            self.nodes = []
        if not hasattr(self, 'edges'):
            self.edges = []

class Switch(Gui):
    def __init__(self,name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)        
        if not hasattr(self,'value'):
            self.value = False
        if not hasattr(self,'type'):
            self.type = 'switch'

class Select(Gui):
    def __init__(self,name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        if not hasattr(self,'options'):             
            self.options = []
        if not hasattr(self,'value'):
            self.value = None
        if not hasattr(self, 'type'):
            self.type = 'select' if len(self.options) > 3 else 'radio'        

class Tree(Gui):
    def __init__(self,name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)         
        self.type = 'tree' 
        if not hasattr(self,'options'):
            self.options = {}        
        if not hasattr(self,'value'):
            self.value = None        
        
class Block(Gui):
    def __init__(self, name, *args, **kwargs):        
        self.name = name        
        self.type = 'block'
        self.value = list(args)        
        self.add(kwargs)  
        if hasattr(self,'scaler'):
            scaler = ContentScaler(elements = lambda: self.scroll_list)
            self.scaler = scaler
            if not self.value:
                self.value = [[scaler]]
            elif isinstance(self.value[0], list):
                self.value[0].append(scaler)
            else:
                self.value[0] = [self.value, scaler]
    @property
    def scroll_list(self):            
        return self.value[1] if len(self.value) > 1 and isinstance(self.value[1], (list, tuple)) else []
    
    @scroll_list.setter
    def scroll_list(self, lst):
        self.value = [self.value[0] if self.value else [], lst]
        if hasattr(self,'scaler'):
            sval = self.scaler.value
            if sval != 1:
                self.scaler.value = 1
                self.scaler.changed(self.scaler, sval)

class ParamBlock(Block):
    def __init__(self, name, row = 3, **params):
        super().__init__(name, [])
        self.name2elem = {}
        cnt = 0        

        for param, val in params.items():                    
            pretty_name = param.replace('_',' ')
            pretty_name = pretty_name[0].upper() + pretty_name[1:]
            t = type(val)
            if t == str:
                el = Edit(pretty_name, val)
            elif t == bool:
                el = Switch(pretty_name, val)
            elif t == list or t == tuple:
                el = Select(pretty_name, val[0], options = val, type = 'select')
            else:
                el = Edit(pretty_name, val, type = 'number')
            self.name2elem[param] = el
            
            if cnt % row == 0:
                block = []
                self.value.append(block)
            cnt += 1
            block.append(el)
    @property
    def params(self):
        return {name: el.value for name, el in self.name2elem.items()}

class Dialog:  
    def __init__(self, question, callback, *content, buttons=['Ok','Cancel'],icon='not_listed_location'):
        self.name = question
        self.callback = callback  
        self.type = 'dialog'         
        self.buttons = buttons        
        self.content = Block(question,[], *content, dialog = True, icon = icon) 

class TextArea(Gui):
    def __init__(self,name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.type = 'textarea' 
                     
class Screen(Gui):
    def __init__(self, name, **kwargs):
        self.name = name
        self.add(kwargs)   
        self.type = 'screen'
