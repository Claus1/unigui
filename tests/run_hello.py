import sys
import os

wd = os.getcwd()
#add 2 path if unigui is installed near
print(wd[:wd.find('/unigui')] + '/unigui')
sys.path.insert(0,wd[:wd.find('/unigui')] + '/unigui')

import unigui

class Hello_user(unigui.User):
    def __init__(self):
        super().__init__()
        print('New Hello user connected and created!')

unigui.start('Test app', user_type = Hello_user)
