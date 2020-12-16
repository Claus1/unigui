from unigui import *

def update(_,val):
    pass

def append(_,val):
    pass


table = Table('Audios', headers = ['Audio', 'Duration', 'Owner', 'Status', 'Links'],rows = [
    ['opt_sync1_3_0.mp3', '237 seconds', 'Admin', 'Processed', 'Refererence 8'],
    ['opt_sync1_3_0.mp3', '639 seconds', 'Admin', 'Processed', 'Refererence 10']
], value = -1, update = update, append = append)

select_concept_mode = Select('Delect', value='All', options=['All','Based','Group'])

def changed(_, value):
    _.value = value
    #return Info(f'Now value is {value}')
    print('ch + ' + value)

def com(_, value):
    return ['aaa', 'bbbb', 'cccccc']

tblock = Block('New block', 
                       
        select_concept_mode,
        Text('Text about cats'),
        Edit('Important', 'Enter something', changed, complete = com)
    , table)

