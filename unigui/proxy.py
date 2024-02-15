from websocket import create_connection
from enum import Enum
from .common import *

class Event(Enum):
    none = 0
    dialog = 1
    screen = 2
    update = 3
    complete = 4
    append = 5
    message = 6
    update_message = 7
    unknown = 8

class Proxy:
    def __init__(self, ip_port, timeout=3):
       assert(ip_port.startswith('ws://') or ip_port.startswith('wss://'))           
       self.conn = create_connection(ip_port, timeout = timeout)
       self.screen = None       
       self.screens = {}
       self.dialog = None
       self.process(self.conn.recv())

    def close(self):
        self.conn.close()

    @property
    def screen_menu(self):
        return [name_icon[0] for name_icon in self.screen['menu']] if self.screen else []
    
    def request(self, message):
        """send message and get responce, return the responce type"""
        self.conn.send(toJson(message))
        responce = self.conn.recv()
        return self.process(responce)
    
    def set_screen(self, name):
        screen = self.screens.get(name)
        if not screen:
            if name in self.screen_menu:
                mtype = self.request(ArgObject(block = 'root', element = None,value = name))
                return mtype == Event.screen 
            else:
                return False
        return True 
       
    def process(self, message):
        message = json.loads(message) 
        self.message = message
        if self.message is None:
            return Event.none
        mtype = message.get('type')        
        self.mtype = mtype
        if mtype == 'screen':
            self.screen = message
            self.screens[self.screen['name']] = message
            message['name2block'] = {block['name']: block for block in flatten(message['blocks'])}
            return Event.screen
        elif mtype == 'dialog':
            self.dialog = message
            return Event.dialog
        elif mtype == 'complete':
            return Event.complete
        elif mtype == 'append':
            return Event.append
        elif mtype == 'update':
            self.update()
            return Event.update
        else:
            updates = message.get('updates')
            if not updates:
                return Event.message
            self.update()         
            if type == 'error' or type == 'warning' or type == 'info':
                return Event.update_message
            return Event.unknown
        
    def update(self):
        """update screen from the message"""
        updates = self.message.get('updates')
        for update in updates:
            path = update['path']
            name2block = self.screen['name2block']
            if len(path) == 1: #block
                name2block[block] = update['data']
            else:
                block, element = path
                name2block[block][element] = update['data']
    
