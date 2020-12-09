import os
from datetime import datetime

resource_port = 1235
appname = 'Unigui'
app_screen_dir = 'screens'

def rindex(mylist, myvalue):
    if myvalue not in mylist:
        return -1
    return len(mylist) - mylist[::-1].index(myvalue) - 1
        
def get_subdirs(dir):
    return [sd for sd in os.listdir(dir) if os.path.isdir(os.path.join(dir, sd))]

def get_file_names(dir, ext, reverse = False):
    '''ext can be .jpg|.png|.xck or just .xxx'''
    if '|' in ext:
        ext = ext.split(sep='|')
        test = lambda fn: any(e for e in ext if fn.endswith(e))
    elif not ext:
        test = lambda fn: True
    else:
        test = lambda fn: fn.endswith(ext)
    files = [x for x in os.listdir(dir) if test(x)]    
    t2f = {os.path.getmtime(dir + '/' + f) : f for f in files}
    times = list(t2f.keys())
    times.sort(reverse = reverse)
    return [t2f[t] for t in times]

def Answer(data, query):
    return {'answer': data,'query': query}

def Error(message):
    return {'error':message}

def Info(message):
    return {'info':message}

def Update(data):
    return {'data': data,'update': None}

def UpdateError(data, message):
    return {'data': data, 'error':message, 'update': None}

def upload_dir():
    os.getcwd() + '/uploads/'

def low_prob(prob):
    return prob < 0.01

UpdateScreen = True

