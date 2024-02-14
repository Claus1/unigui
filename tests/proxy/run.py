import os, sys

#optional:  add 2 path if unigui is installed near (for deep testing or developing)
wd = os.getcwd()
print(wd[:wd.find('/unigui')] + '/unigui')
sys.path.insert(0,wd[:wd.find('/unigui')] + '/unigui')

from unisi import *
proxy = Proxy('ws://localhost:8000/ws')
vv = proxy.set_screen('Zoo')
proxy.close()