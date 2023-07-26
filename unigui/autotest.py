import config, os, logging
from .utils import *
from .guielements import * 
from .users import User
from jsoncomparison import Compare, NO_DIFF

#setting config variables
testdir = 'autotest'
if not hasattr(config, testdir):
    config.autotest = False
if not hasattr(config, 'port'):
    config.port = 8000
if not hasattr(config, 'pretty_print'):
    config.pretty_print = config.autotest
if not hasattr(config, 'upload_dir'):
    config.upload_dir = 'web'
if not hasattr(config, 'logfile'):
    config.logfile = None
if not hasattr(config, 'hot_reload'):
    config.hot_reload = False
if not hasattr(config, 'appname'):
    config.appname = 'Unigui app'
if not hasattr(config, 'mirror'):
    config.mirror = False

if not os.path.exists(config.upload_dir):
    os.makedirs(config.upload_dir)

#start logging 
format = "%(asctime)s - %(levelname)s - %(message)s"
logfile = config.logfile
handlers = [logging.FileHandler(logfile), logging.StreamHandler()] if logfile else []
logging.basicConfig(level = logging.WARNING, format = format, handlers = handlers)

comparator = Compare().check

def jsonString(obj):
    pretty = config.pretty_print
    return toJson(obj, 2 if pretty else 0, pretty)

class Recorder:
    def __init__(self):
        self.start(None)
        
    def accept(self, msg, response):        
        if self.ignored_1message:            
            self.record_buffer.append(f"{jsonString(msg)},\
                \n{'null' if response is None else jsonString(response)}\n")
        else: #start for setting screen
            self.record_buffer.append(jsonString(['root', User.last_user.screen_module.name]))
            self.ignored_1message = True    

    def stop_recording(self, _, x):    
        button.mode = None
        button.changed = button_clicked
        button.tooltip = 'Create autotest'
        with open(self.record_file, mode='w') as file:    
            content = ',\n'.join(self.record_buffer)
            file.write(f"[\n{content}]")
        test_name = self.record_file
        self.record_file = None
        return Info(f'Test {test_name} is created.', button)

    def start(self,fname):
        self.record_file = fname
        self.ignored_1message = False
        self.record_buffer = []

recorder = Recorder()

def obj2pyjson(obj):
    return json.loads(jsonpickle.encode(obj,unpicklable=False))

def test(filename, user):
    filepath = f'{testdir}{divpath}{filename}'
    file = open(filepath, "r") 
    data = json.loads(file.read())
    error = False
    for message in data:
        if isinstance(message, list):
            result = user.result4message(message)
            response = user.prepare_result(result)
            user_message = message
        else:
            diff = comparator(obj2pyjson(response), message)
            if diff != NO_DIFF:
                err = diff.get('_message')
                if not err:
                    for value in diff.values():
                        err = value['_message']
                        print(f"\nTest {filename} is failed on message {user_message}!\n {err}\n")
    return not error

test_name = Edit('Name test file', '', focus = True)
rewrite = Switch('Overwrite existing', False, type = 'check')

def button_clicked(_,__):
    test_name.value = ''
    test_name.complete = smart_complete(os.listdir(testdir))
    return Dialog('Create autotest..', ask_create_test, test_name, rewrite)

def create_test(fname):
    fname = f'{testdir}{divpath}{fname}'    
    if os.path.exists(fname) and not rewrite.value:
        return Warning(f'Test file {fname} already exists!')              
    
    button.mode = 'red'   
    button.tooltip = 'Stop test recording'
    button.changed = recorder.stop_recording
    recorder.start(fname)
    
    return Info('Recording is running.. press the same button to stop',button)     

def ask_create_test(_, bname):
    if bname == 'Ok':            
        return create_test(test_name.value) if test_name.value else\
            Warning('Test file name is not defined!')

button = Button('_Add test', button_clicked, 
        icon='data_saver_on', tooltip='Create autotest')

def check_dialog(self):
    errors = []
    child_names = set()   
    tt = type(self)   
    if not hasattr(self, 'name') or not self.name:            
        errors.append(f"The block with {[str(type(gui)).split('.')[-1] for gui in flatten(self.value)]} does not contain name!")
        self.name = 'Unknown'          
    if not isinstance(self.name, str):
        errors.append(f"The block with name {self.name} is not a string!")
    for child in flatten(self.value):           
        if not isinstance(child, Gui) or not child:
            errors.append(f'The block {self.name} contains invalid element {child} instead of Gui+ object!') 
        elif isinstance(child, Block):
            errors.append(f'The block {self.name} contains block {child.name}. Blocks cannot contain blocks!')                                                                                                       
        elif child.name in child_names:                        
            errors.append(f'The block {self.name} contains a duplicated element name "{child.name}"!')
        else:
            child_names.add(child.name)                
    return errors

def check_screen(module):
    self = module.screen
    errors =  []        
    block_names = set()        
    if not hasattr(self, 'name') or not self.name:            
        errors.append(f"Screen file {module.__file__} does not contain name!")
        self.name = 'Unknown'
    if not isinstance(self.name, str):
        errors.append(f"The name in screen file {module.__file__} {self.name} is not a string!")
    if not isinstance(self.blocks, list):
        errors.append("Screen file {self.__module__.__file__} does not contain name!")
    else:
        for bl in flatten(self.blocks):            
            if not isinstance(bl, Block):
                errors.append(f'The screen contains invalid element {bl} instead of Block object!')                                                    
            elif bl.name in block_names:
                errors.append(f'The screen contains a duplicated block name {bl.name}!')    
            else:            
                block_names.add(bl.name)
            errors += check_dialog(bl)
    if errors:
        errors.insert(0, f"\nErrors in screen {self.name}, file name {module.__file__}:")
    return errors
    
def run_tests():
    if not os.path.exists(testdir):
        os.makedirs(testdir)
    user = User.UserType()
    user.load()
    errors = []
    for module in user.screens:
        errors += check_screen(module)
    if errors:
        errors.insert(0, f'\n!!----Unigui detected errors in screens:')
        print('\n'.join(errors), '\n')
    elif user.screens:
        print(f'\n----Screens definitions are correct. ')
        
    files = config.autotest
    ok = True
    process = False
    if os.path.exists(testdir):
        for file in os.listdir(testdir):
            if not os.path.isdir(file) and (files == '*' or file in files):
                process = True
                if not test(file,user):
                    ok = False
    if process and ok:
        print('-----Autotests successfully passed.-----')
    User.last_user = None
    User.toolbar.append(button)
    
        

            