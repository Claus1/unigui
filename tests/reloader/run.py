import os, sys
from urllib import request

#optional:  add 2 path if unigui is installed near (for deep testing or developing)
wd = os.getcwd()
print(wd[:wd.find('/unigui')] + '/unigui')
sys.path.insert(0,wd[:wd.find('/unigui')] + '/unigui')

import unigui
from unigui import User

import sys
import time
import logging
import asyncio
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from threading import Thread

loop = asyncio.new_event_loop()
def f(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever() 

t = Thread(target=f, args=(loop,))
t.start()  

def free():
    global busy
    if request_file:
        reload(request_file)

busy = False        

def reload(sname):
    global busy, request_file
    busy = True
    request_file = None
    user = User.last_user
    try:
        module = user.load_module(sname)
    except:
        return
    user.screens[0] = module
    user.set_screen(module.name)
    asyncio.run_coroutine_threadsafe(user.send(True), loop)     

    time.sleep(3)
    free()    

class ScreenEventHandler(PatternMatchingEventHandler):    
    def on_modified(self, event):
        global busy, request_file
        super(ScreenEventHandler, self).on_modified(event)
        arr = event.src_path.split('/')
        if len(arr) > 1: 
            if busy:
                request_file = arr[1]
            else:
                reload(arr[1])            

logging.basicConfig(level=logging.INFO)
event_handler = ScreenEventHandler()
observer = Observer()
observer.schedule(event_handler, 'screens')
observer.start()
    
unigui.start('Test app')
observer.join()