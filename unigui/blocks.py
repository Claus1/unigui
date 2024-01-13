from .guielements import Gui, Range, Edit, Switch, Select

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
    def __init__(self, name, *args, row = 3, **params):
        if not args:
            args = [[]]
        super().__init__(name, *args)
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
    def __init__(self, question, callback, *content, buttons=['Ok','Cancel'],
            icon='not_listed_location'):
        self.name = question
        self.callback = callback  
        self.type = 'dialog'         
        self.buttons = buttons        
        self.content = Block(question,[], *content, dialog = True, icon = icon) 

class Screen:
    def __init__(self, name, **kwargs):
        self.name = name
        self.type = 'screen'
        for key, value in kwargs.items():
            setattr(self, key, value) 

