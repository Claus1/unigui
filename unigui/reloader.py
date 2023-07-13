import logging, os, traceback
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from unigui import User

import config

hot_reload = 'hot_reload'

if hasattr(config, hot_reload) and config.hot_reload:
    busy = False        

    def free():
        global busy
        if request_file:
            reload(request_file)
        else:
            busy = False

    def reload(sname):
        user = User.last_user
        if user:
            global busy, request_file
            busy = True
            request_file = None
            
            try:
                module = user.load_module(sname)
            except:
                busy = False
                traceback.print_exc()        
                return

            for i, s in enumerate(user.screens):
                if s.__file__ == module.__file__:
                    same = user.screen_module.__file__ == module.__file__
                    user.screens[i] = module
                    if same:
                        user.set_screen(module.screen.name)            
                    break
            else:
                user.screens.append(module)

            user.update_menu()
            user.set_clean() 
            user.sync_send(True)

            free()  
            return module  

    class ScreenEventHandler(PatternMatchingEventHandler):    
        def on_modified(self, event):
            if not event.is_directory and hasattr(User,'last_user'):            
                arr = event.src_path.split('/') 
                name = arr[-1]
                dir = arr[-2]  
                if name.endswith('.py') and dir in ['screens','blocks']:         
                    super(ScreenEventHandler, self).on_modified(event)
                    if busy:
                        global request_file            
                        request_file = f'{dir}/{name}' 
                    else:                    
                        fresh_module = reload(name) if dir == 'screens' else None                    
                        current = User.last_user.screen_module.__file__
                        if not fresh_module or current != fresh_module.__file__:
                            reload(current.split('/')[-1])             

    logging.basicConfig(level=logging.INFO)
    event_handler = ScreenEventHandler()
    observer = Observer()
    path = os.getcwd()
    observer.schedule(event_handler, path, recursive = True)
    observer.start()
    