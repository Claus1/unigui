class Gui:
    def __init__(self, *args, **kwargs):
        self.name = args[0]
        la = len(args)
        if la > 1:
            self.value = args[1]
        if la > 2:
            self.changed = args[2]                    
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
        self.value = self.name
        self.type = 'text'        

class Button(Gui):
    def __init__(self, *args, **kwargs):
        self.name = args[0]
        self.add(kwargs)
        if not hasattr(self, 'type'):
            self.type = 'button'
        if len(args) > 1 and not hasattr(self, 'changed'):
            self.changed = args[1]        
            
def CameraButton(name, *args, **kwargs):    
    kwargs['type'] = 'camera'
    return Button(name, *args, **kwargs)
        
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
        if not hasattr(self,'type'):
            self.type = 'switch'

class Select(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self,'options'):             
            self.options = []
        if not hasattr(self,'value'):
            self.value = None
        if not hasattr(self, 'type'):
            self.type = 'select' if len(self.options) > 3 else 'radio'        

class Tree(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)         
        self.type = 'tree' 
        if not hasattr(self,'options'):
            self.options = {}        
        if not hasattr(self,'value'):
            self.value = None        
        
class Block(Gui):
    def __init__(self, *args, **kwargs):        
        self.name = args[0]        
        self.type = 'block'
        self.value = list(args[1:])        
        self.add(kwargs)        

class Dialog:  
    def __init__(self,name,callback,*content,buttons=['Ok','Cancel'],icon='not_listed_location'):
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
        self.name = args[0] if args else ''               
        self.add(kwargs)   
        self.type = 'screen'
