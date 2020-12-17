from unigui import *

def append(_,val):
    pass

def updated(_, value):
    print(f'updated {value}!')

def complete(_, value):
    return ['aaa', 'bbbb', 'cccccc']

def changed(_, value):
    _.value = value
    print(f'ch {value}')


table = Table('Audios', -1, changed, headers = ['Audio', 'Duration', 'Owner', 'Status', 'Links'],rows = [
    ['opt_sync1_3_0.mp3', '237 seconds', 'Admin', 'Processed', 'Refererence 8'],
    ['opt_sync1_3_0.mp3', '639 seconds', 'Admin', 'Processed', 'Refererence 10']
], update = updated, append = append, complete = complete)


tblock = Block('New block',                        
        Edit('Simple update', 'cherokke', update = updated),
        Text('Text about cats'),
        Edit('Complete enter', 'Enter something', changed, update = updated, complete = complete)
    , table)

