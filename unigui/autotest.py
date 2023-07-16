import config, os
from .guielements import * 
from .users import User
from .utils import *

testdir = 'autotest'
if not os.path.exists(testdir):
    os.makedirs(testdir)

record_file = None
ignored_1message = False
record_buffer = []

def test(file):
    pass

def recorder(msg, response):
    if record_file:
        global ignored_1message, record_buffer
        if ignored_1message:            
            record_buffer.append(f'{msg},\n{response}')
        else:
            ignored_1message = True

def alltest():    
    files = config[testdir]
    for file in os.listdir(testdir):
        if  file == '*' or file in files:
            test(file)

edit = Edit('Name test file', '')
rewrite = Switch('Overwrite existing', False, type = 'check')

def button_clicked(x,y):
    edit.value = ''
    edit.complete = smart_complete(os.listdir(testdir))
    return Dialog('Create autotest..', ask_create_test, edit, rewrite)

def stop_recording(_, x):
    global record_file, record_buffer, button
    button.mode = None
    button.changed = button_clicked
    button.tooltip = 'Create autotest'
    with open(record_file, mode='w') as file:    
        file.write(f"{{{',\n'.join(record_buffer)}}}")
    record_file = None
    return True

def create_test(fname):
    fname = f'{testdir}/{fname}'
    if os.path.exists(fname) and not rewrite.value:
        return Warning(f'Test file {fname} already exists!')
    user = User.last_user
    if user.screen_module is not user.screens[0]:
        return Warning('Test has to started from the first screen!') 
    global record_file, ignored_1message, record_buffer
    record_file = fname
    button.mode = 'red'   
    button.tooltip = 'Stop recording test'
    button.changed = stop_recording
    ignored_1message = False
    record_buffer = []
    return True     

def ask_create_test(_, bname):
    if bname == 'Ok':            
        return create_test(edit.value) if edit.value else Warning('Test file name is not defined!')

button = Button('_Add test', button_clicked, 
        icon='data_saver_on', tooltip='Create autotest')
        
if hasattr(config, testdir):                        
    User.toolbar.append(button)

    
        

            