import config, os, logging
from .utils import *
from .guielements import * 
from .users import User

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
handlers = [logging.FileHandler(config.logfile), logging.StreamHandler()] if config.logfile else []
logging.basicConfig(level = logging.WARNING, format = format, handlers = handlers)

record_file = None
ignored_1message = False
record_buffer = []

def recorder(msg, response):
    if record_file:
        global ignored_1message, record_buffer
        if ignored_1message:            
            record_buffer.append(f'{msg},\n{"null" if response is None else response}\n')
        else:
            record_buffer.append(['root', User.last_user.screen_module.name])# where to start
            ignored_1message = True

if config.autotest:
    if not os.path.exists(testdir):
        os.makedirs(testdir)
    user = User()
    user.load()

    def test(filename):
        file = open(filename, "r") 
        data = json.loads(file.read())
        for message in data:
            if isinstance(message, list):
                respponse = user.process(message)
                

    def alltest():    
        files = config.autotest
        for file in os.listdir(testdir):
            if not os.path.isdir(file) and (files == '*' or file in files):
                test(file)

    test_name = Edit('Name test file', '')
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
            file.write(f"{{\n{content}}}")
        record_file = None
        return button

    def create_test(fname):
        fname = f'{testdir}/{fname}'
        if os.path.exists(fname) and not rewrite.value:
            return Warning(f'Test file {fname} already exists!')
        user = User.last_user
        if not user.screen_module:
            return Warning('Test has to started on some screen!') 
        global record_file, ignored_1message, record_buffer
        record_file = fname
        button.mode = 'red'   
        button.tooltip = 'Stop recording test'
        button.changed = stop_recording
        ignored_1message = False
        record_buffer = []
        return button     

    def ask_create_test(_, bname):
        if bname == 'Ok':            
            return create_test(test_name.value) if test_name.value else\
                Warning('Test file name is not defined!')

    button = Button('_Add test', button_clicked, 
            icon='data_saver_on', tooltip='Create autotest')
                                    
    User.toolbar.append(button)

    
        

            