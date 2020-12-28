from unigui import *

def append(_,val):
    pass

def updated(_, value):
    return Warning(f'{_.name} is updated to {value}!')        

def complete(_, value):
    return ['aaa', 'bbbb', 'cccccc']

def changed(_, value):
    _.value = value  

def table_update(_, value):
    value, pos = value
    if not value.isdigit():
        return 'only int!'

def dialog_callback(_,button_name):
    return Warning(f'Dialog: {button_name} pushed!')

def call_dialog(*_):
    return Dialog('Dialog', 'Answer please..', dialog_callback, buttons = ['Yes','No'])

table = Table('Audios', -1, changed, headers = ['Audio', 'Duration,sec'],rows = [
    ['opt_sync1_3_0.mp3', '237'],
    ['opt_sync1_3_0.mp3', '639']
],  append = append, complete = complete, update = table_update, modify = table_update, tools = False)

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

tree = Tree('Inharitance','Animals', lambda _,v: Info(f'{v} selected!'), unique_elems = ld)

tblock = Block('New block',                        
        [Button('Dialog', call_dialog), Edit('Simple Enter update', 'cherokke', update = updated)],
        Text('Text about cats'),
        Edit('Read only', 'Try to change me!', edit = False),
        Edit('Complete enter update field', 'Enter something', changed, complete = complete, update = updated)
    , [tree, table])

