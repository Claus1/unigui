import config, os
from .guielements import * 
from .users import User
from .utils import *

testdir = 'autotest'
autotest = getattr(config, testdir, False)
record_file = None
ignored_1message = False
record_buffer = []

def recorder(msg, response):
    if record_file:
        global ignored_1message, record_buffer
        if ignored_1message:            
            record_buffer.append(f'{msg},\n{"null" if response is None else response}\n')
        else:
            ignored_1message = True

if autotest:
    if not os.path.exists(testdir):
        os.makedirs(testdir)

    def test(file):
        pass

    def alltest():    
        files = config[testdir]
        for file in os.listdir(testdir):
            if  files == '*' or file in files:
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
        if user.screen_module is not user.screens[0]:
            return Warning('Test has to started from the first screen!') 
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

    
        

            