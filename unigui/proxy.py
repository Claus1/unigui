from websocket import create_connection
from enum import Enum

from .common import *

class Event(Enum):
    none = 0
    update = 1
    invalid = 2
    message = 4
    unknown = 8
    dialog = 16
    screen = 32
    update_message = 6
    complete = 64
    append = 128    

ws_header = 'ws://'
wss_header = 'wss://'
ws_path = 'ws'

message_types = ['error','warning','info','progress']

class Proxy:
    def __init__(self, addr_port, timeout = 3, ssl = False):
       if not addr_port.startswith(ws_header) and not addr_port.startswith(wss_header):
           addr_port = f'{wss_header if ssl else ws_header}{addr_port}'
           addr_port = f'{addr_port}{"" if addr_port.endswith("/") else "/"}{ws_path}'
                      
       self.conn = create_connection(addr_port, timeout = timeout)
       self.screen = None       
       self.screens = {}
       self.dialog = None
       self.request(None)

    def close(self):
        self.conn.close()

    @property
    def screen_menu(self):
        return [name_icon[0] for name_icon in self.screen['menu']] if self.screen else []
    
    @property
    def commands(self, names = False):
        """return command objects or its names"""
        celems = self.elements(types=['command'])        
        return [el['name'] for el in celems] if names else celems        
    
    def elements(self, block = None, types = None):
        """get elements with filtering types and blocks"""
        if block:
            return [el for el in flatten(block['value']) if not types or el['type'] in types]
        answer = []
        for block in self.screen['name2block'].values(): 
            answer.extend([el for el in flatten(block['value']) if not types or el['type'] in types])
        return answer
    
    def block_of(self, element):
        for block in self.screen['name2block'].values():
            for el in flatten(block['value']):
                if el == element:
                    return block
    
    def action(self, element, value, event = 'changed'):
        if event != 'changed' and event not in element:
            return Event.invalid
        return self.request(ArgObject(block = self.block_of(element), element = element['name'], 
            event = event, value = value))

    def request(self, message):
        """send message and get responce, return the responce type"""
        if message:
            self.conn.send(toJson(message))
        responce = self.conn.recv()
        message = json.loads(responce) 
        return self.process(message) if message else Event.none
    
    def set_screen(self, name):
        screen = self.screens.get(name)
        if not screen:
            if name in self.screen_menu:
                mtype = self.request(ArgObject(block = 'root', element = None, value = name))
                return mtype == Event.screen 
            else:
                return False
        return True 
       
    def process(self, message):        
        self.message = message        
        mtype = message.get('type')        
        self.mtype = mtype
        if mtype == 'screen':
            self.screen = message
            self.screens[self.screen['name']] = message
            name2block = {block['name']: block for block in flatten(message['blocks'])}            
            name2block['toolbar'] = {'name': 'toolbar', 'value': message['toolbar']}
            message['name2block'] = name2block
            return Event.screen
        elif mtype == 'dialog':
            self.dialog = message
            return Event.dialog
        elif mtype == 'complete':
            return Event.complete
        elif mtype == 'append':
            return Event.append
        elif mtype == 'update':
            self.update(message)
            return Event.update
        else:
            updates = message.get('updates')
            if not updates:
                return Event.message
            self.update(message)         
            return Event.update_message if type in message_types else Event.unknown
        
    def update(self, message):
        """update screen from the message"""
        updates = message.updates
        for update in updates:
            path = update['path']
            name2block = self.screen['name2block']
            if len(path) == 1: #block
                name2block[block] = update['data']
            else:
                block, element = path
                name2block[block][element] = update['data']
    
