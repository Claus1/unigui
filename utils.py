import os
from datetime import datetime

resource_port = 1235

def rindex(mylist, myvalue):
    if myvalue not in mylist:
        return -1
    return len(mylist) - mylist[::-1].index(myvalue) - 1

def fn2url(fn):
    arr = fn.split('/')
    ind = rindex(arr, 'images') 
    if ind < 0:
        arr.insert(0,'images')   
    else:
        arr = arr[ind:]
    s =  f":{resource_port}/{'/'.join(arr)}"
    return s.replace(' ','%20')

binfile = "kbases/current.bin"
initfile = "kbases/init.bin"
kbasedir = "kbases/"
kbaseext = '.change'

states_dir = 'states/'
cond_ext = '.cond'
        
def get_subdirs(dir):
    return [sd for sd in os.listdir(dir) if os.path.isdir(os.path.join(dir, sd))]

def get_file_names(reverse = False, dir = kbasedir, ext = kbaseext):
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

def get_next_file_name(dir = kbasedir, ext = kbaseext):
    files = get_file_names(False, dir, ext)
    fname = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
    return dir + fname + ext

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

str_probs = ['Very high', 'High','Low','Very low']

def low_prob(prob):
    return prob < 0.01

def prob2str(prob):
    if prob >= 0.5:
        s = str_probs[0]
    elif prob >= 0.1:
        s = str_probs[1]
    elif prob >= 0.01:
        s = str_probs[2]
    else:
        s = str_probs[3]
    return s

UpdateScreen = True

