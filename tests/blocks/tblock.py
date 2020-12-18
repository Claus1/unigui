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

table = Table('Audios', -1, changed, headers = ['Audio', 'Duration', 'Owner', 'Status', 'Links'],rows = [
    ['opt_sync1_3_0.mp3', '237 seconds', 'Admin', 'Processed', 'Refererence 8'],
    ['opt_sync1_3_0.mp3', '639 seconds', 'Admin', 'Processed', 'Refererence 10']
],  append = append, complete = complete, update = tupd, modify = tupd)

tblock = Block('New block',                        
        [Button('Dialog', call_dialog), Edit('Simple update', 'cherokke', update = updated)],
        Text('Text about cats'),
        Edit('Complete enter', 'Enter something', changed, complete = complete)
    , table)

