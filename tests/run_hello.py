import sys
import os

#add parent path where unigui is
#hack until unigui is not in python repository
parent_dir_lib = os.getcwd()[:-13]
sys.path.insert(0, parent_dir_lib)

import unigui

unigui.start('Test app', screen_dir = 'screens_hello')
