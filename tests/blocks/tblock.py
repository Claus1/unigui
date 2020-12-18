from unigui import *

def append(_,val):
    pass

def updated(_, value):
    print(f'updated {value}!')
    if not value.isdigit():
        return 'only int!'

def complete(_, value):
    return ['aaa', 'bbbb', 'cccccc']

def changed(_, value):
    _.value = value
    print(f'ch {value}')

def tupd(_, value):
    value, pos = value
    if not value.isdigit():
        return 'only int!'

def dialog_callback(_,button_name):
    return Warning(f'Dialog: {button_name} pushed!')

def call_dialog(*_):
    return Dialog('Dialog', 'Answer please', dialog_callback, buttons = ['Yes','No'])

table = Table('Audios', -1, changed, headers = ['Audio', 'Duration,sec'],rows = [
    ['opt_sync1_3_0.mp3', '237'],
    ['opt_sync1_3_0.mp3', '639']
],  append = append, complete = complete, update = tupd, modify = tupd)

ld = { 'Mammals' : None,
    'Brushtail Possum' : 'Mammals',
'Genet' : 'Mammals',
'Silky Anteater' : 'Mammals',
'Greater Glider' : 'Mammals',
'Tarsier' : 'Mammals',
'Kinkajou' : 'Mammals',
'Tree Kangaroo' : 'Mammals',
'Sunda Flying Lemur' : 'Mammals',
'Green Tree Python' : 'Mammals',
'Fruit Bat' : 'Mammals',
'Tree Porcupines' : 'Mammals',
'Small Tarsier' : 'Tarsier',
'Very small Tarsier': 'Small Tarsier'
}

tree = Tree('Inharitance','Mammals', lambda _,v: Info(f'{v} selected!'), unique_elems = ld)

tblock = Block('New block',                        
        [Button('Dialog', call_dialog), Edit('Simple update', 'cherokke', update = updated)],
        Text('Text about cats'),
        Edit('Complete enter', 'Enter something', changed, complete = complete)
    , [tree, table])

