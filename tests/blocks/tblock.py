from unigui import *
import time
user = get_user()

def append(_,val):
    pass

def updated(_, value):
    return Warning(f'{_.name} is updated to {value}!')        

def complete(_, value):
    value = value[0]
    if value and isinstance(value, str) and len(value) > 2 and value[0].isalpha():
        return ['aaa', 'bbbb', 'cccccc']
    return []

def complete_edit(_, value):    
    return ['value 21', 'sum 289', 'absolute 3']
    

def changed(_, value):
    _.value = value  
    return Warning(f'{_.name} changed to {value}!')

def table_modify(_, value):
    value, pos = value    
    return Error(f'{_.name} {pos} is not modified to value {value}!')

def table_update(_, value):    
    accept_rowvalue(_, value)
    value, pos = value        
    return Info(f'{_.name} {pos} is updated to value {value}!')

def dialog_callback(_,button_name):
    perstr = lambda per : 'Process executing {}%'.format(per)
    if button_name == 'Yes':
        user.progress(perstr(0))
        for i in range(100):
            user.progress(perstr(i))
            time.sleep(0.02)
    return user.progress(None)

def call_dialog(*_):
    return Dialog('Dialog', 'Start a long process?', dialog_callback, buttons = ['Yes','No'])

def delete_row(_,v):
    del _.rows[_.value]
    return _

import random

table = Table('Audios', 0, changed, headers = ['Audio', 'Duration,sec', 'Stars'],
rows =  [[f'sync{i}.mp3', round(random.random() * 15000) / 100, random.randint(1,50)] for i in range(100)],
append = append, complete = complete, update = table_update, delete = delete_row, view = 'i-1,2')

ld = { 
    'Animals' : None,
    'Brushtail Possum' : 'Animals',
    'Genet' : 'Animals',
    'Silky Anteater' : 'Animals',
    'Greater Glider' : 'Animals',
    'Tarsier' : 'Animals',
    'Kinkajou' : 'Animals',
    'Tree Kangaroo' : 'Animals',
    'Sunda Flying Lemur' : 'Animals',
    'Green Tree Python' : 'Animals',
    'Fruit Bat' : 'Animals',
    'Tree Porcupines' : 'Animals',
    'Small Tarsier' : 'Tarsier',
    'Very small Tarsier': 'Small Tarsier'
}

tree = Tree('Inheritance','Animals', lambda _,v: Info(f'{v} selected!'), unique_elems = ld)

eblock = Block('New block',                        
        [Button('Dialog for a process', call_dialog), Edit('Simple Enter update', 'cherokke', update = updated)],
        Text('Text about cats'),
        Edit('Read only', 'Try to change me!', edit = False),
        Edit('Complete enter update field', 'Enter something', changed, complete = complete_edit, update = updated)
)

treeblock = Block('Tree block',[], tree, icon = 'account_tree')

tableblock = Block('Table chart - push the chart button on the table..', [], table, icon = 'insights')

config_area = [eblock, [treeblock, tableblock]]

