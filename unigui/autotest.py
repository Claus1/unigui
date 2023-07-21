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

record_file = None
ignored_1message = False
record_buffer = []
comparator = Compare().check

def jsonString(obj):
    pretty = config.pretty_print
    return toJson(obj, 2 if pretty else 0, pretty)

def recorder(msg, response):
    if record_file:
        global ignored_1message, record_buffer
        if ignored_1message:            
            record_buffer.append(f"{jsonString(msg)},\
                \n{'null' if response is None else jsonString(response)}\n")
        else: #start for setting screen
            record_buffer.append(jsonString(['root', User.last_user.screen_module.name]))
            ignored_1message = True    

def obj2pyjson(obj):
    return json.loads(jsonpickle.encode(obj,unpicklable=False))

def test(filename, user):
    filepath = f'{testdir}{divpath}{filename}'
    file = open(filepath, "r") 
    data = json.loads(file.read())
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
                    err = diff['type']['_message']
                print(f"\nTest {filename} is failed on message {user_message}!\n {err}\n")
                return False
    return True

test_name = Edit('Name test file', '', focus = True)
rewrite = Switch('Overwrite existing', False, type = 'check')

def button_clicked(x,y):
    test_name.value = ''
    test_name.complete = smart_complete(os.listdir(testdir))
    return Dialog('Create autotest..', ask_create_test, test_name, rewrite)

def stop_recording(_, x):
    global record_file, record_buffer, button
    button.mode = None
    button.changed = button_clicked
    button.tooltip = 'Create autotest'
    with open(record_file, mode='w') as file:    
        content = ',\n'.join(record_buffer)
        file.write(f"[\n{content}]")
    test_name = record_file
    record_file = None
    return Info(f'Test {test_name} is created.', button)

def create_test(fname):
    fname = f'{testdir}/{fname}'
    if not os.path.exists(testdir):
        os.makedirs(testdir)
    if os.path.exists(fname) and not rewrite.value:
        return Warning(f'Test file {fname} already exists!')              
    global record_file, ignored_1message, record_buffer
    record_file = fname
    button.mode = 'red'   
    button.tooltip = 'Stop test recording'
    button.changed = stop_recording
    ignored_1message = False
    record_buffer = []
    return Info('Recording is running.. ',button)     

def ask_create_test(_, bname):
    if bname == 'Ok':            
        return create_test(test_name.value) if test_name.value else\
            Warning('Test file name is not defined!')

button = Button('_Add test', button_clicked, 
        icon='data_saver_on', tooltip='Create autotest')
    
def run_tests():
    user = User.UserType()
    user.load()

    for module in user.screens:
        teststr = module.screen.check()
        if teststr:
            print(f'Detected error in screen {module.__file__}:\n{teststr}')
    files = config.autotest
    ok = True
    process = False
    for file in os.listdir(testdir):
        if not os.path.isdir(file) and (files == '*' or file in files):
            process = True
            if not test(file,user):
                ok = False
    if process and ok:
        print('-----Autotests successfully passed.-----')

    if not os.path.exists(testdir):
        os.makedirs(testdir)                                
    User.toolbar.append(button)
    
        

            