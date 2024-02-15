import json, jsonpickle

def flatten(*arr):
    for a in arr:
        if isinstance(a, list):
            yield from flatten(*a)
        else:
            yield a
            
class ArgObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value) 

class ReceivedMessage:
    def __init__(self, data):
        self.screen = data.get('screen')
        self.block = data.get('block')
        self.element = data.get('element')
        self.event = data.get('event')
        self.value = data.get('value')  

def toJson(obj, indent = 0, pretty = False):
    js = jsonpickle.encode(obj,unpicklable=False)
    return json.dumps(json.loads(js), indent=indent, sort_keys=pretty) if pretty else js



