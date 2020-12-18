import sys
import os
wd = os.getcwd()
#add 2 path if unigui not installed
sys.path.insert(0,wd[:wd.find('/unigui/tests')])
import unigui
unigui.start('Test app')
