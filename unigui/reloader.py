from .autotest import config

empty_app = {
    "blocks": [],
    "header": "No screens",
    "icon": None,
    "menu": [["You need to put at least 1 file in the 'screens' folder.",'exclamation']],
    "name": "",
    "order": 0,
    "toolbar": [],
    "type": "screen"
}

if config.hot_reload:
    import os, sys, traceback
    from watchdog.observers import Observer
    from watchdog.events import PatternMatchingEventHandler
    from .users import User
    from .utils import divpath
    import re
    
    busy = False      
    cwd = os.getcwd()  

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
                module = user.load_screen(sname)
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
                if len(user.screens) == 1:
                    user.set_screen(module.name)                    

            user.update_menu()
            user.set_clean() 
            user.sync_send(True)

            free()  
            return module  

    class ScreenEventHandler(PatternMatchingEventHandler):    
        def on_modified(self, event):
            if not event.is_directory and hasattr(User,'last_user'):                            
                short_path = event.src_path[len(cwd) + 1:]
                arr = short_path.split(divpath) 
                name = arr[-1]
                dir = arr[0] if len(arr) > 1 else '' 
                                
                if name.endswith('.py'):
                    user = User.last_user
                    
                    if dir not in ['screens','blocks']: #analyze if dependency exist
                        file = open(user.screen_module.__file__, "r") 
                        arr[-1] = arr[-1][:-3]
                        module_name = '.'.join(arr) 
                        module_pattern = '\.'.join(arr)                        
                        
                        if re.search(f"((import|from)[ \t]*{module_pattern}[ \t\n]*)",file.read()):
                            if module_name in sys.modules:
                                del sys.modules[module_name]                            
                            short_path = user.screen_module.__file__
                            dir, name = short_path.split(divpath)                            

                    if dir in ['screens','blocks']:                             
                        if busy:
                            global request_file            
                            request_file = short_path 
                        else:                    
                            fresh_module = reload(name) if dir == 'screens' else None                                            
                            module = user.screen_module
                            if module:
                                current = module.__file__
                                if not fresh_module or current != fresh_module.__file__:
                                    reload(current.split(divpath)[-1]) 
                                                    
        def on_deleted(self, event):            
            if not event.is_directory and hasattr(User,'last_user'):
                user = User.last_user            
                arr = event.src_path.split(divpath) 
                name = arr[-1]
                dir = arr[-2]  
                if name.endswith('.py') and dir == 'screens':
                    delfile = f'{dir}/{name}'
                    for i, s in enumerate(user.screens):
                        if s.__file__ == delfile:
                            user.screens.remove(s)
                            if user.screen_module is s:
                                if user.screens:                                                                        
                                    fname = user.screens[0].__file__.split(divpath)[-1]
                                    module = reload(fname)
                                    user.set_screen(module.name)
                                    user.update_menu()                                
                                    user.sync_send(True)      
                                else:                                                      
                                    user.sync_send(empty_app)                                                        
                            else:
                                reload(user.screen_module.__file__.split(divpath)[-1])
                                user.update_menu()
                                user.sync_send(True)                                                        
                            break
    
    event_handler = ScreenEventHandler()
    observer = Observer()
    path = os.getcwd()
    observer.schedule(event_handler, path, recursive = True)
    observer.start()
    