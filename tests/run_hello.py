import sys
import os
wd = os.getcwd()
#for testing works with local lib, not installed
sys.path.insert(0,wd[:wd.find('/unigui/tests')])
import unigui

class Hello_user(unigui.User):
    def __init__(self):
        super().__init__()
        print('New Hello user connected and created!')

unigui.start('Test app', user_type = Hello_user, upload_dir = 'images')
