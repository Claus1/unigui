import os, sys
from urllib import request

#optional:  add 2 path if unigui is installed near (for deep testing or developing)
wd = os.getcwd()
print(wd[:wd.find('/unigui')] + '/unigui')
sys.path.insert(0,wd[:wd.find('/unigui')] + '/unigui')

import unigui
from unigui import User

import sys
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import traceback

busy = False        

def free():
    global busy
    if request_file:
        reload(request_file)
    else:
        busy = False

def reload(sname):
    global busy, request_file
    busy = True
    request_file = None
    user = User.last_user
    try:
        module = user.load_module(sname)
    except:
        busy = False
        traceback.print_exc()
        #print(str(e))
        return

    for i, s in enumerate(user.screens):
        if s.name == module.name:
            user.screens[i] = module
            break

    user.set_screen(module.name)
    user.update_menu()
    user.clean_sys4next_user() 
    user.sync_send(True)
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