from unigui import *
from blocks.tblock import tblock
user = get_user()

name = "Main"
icon = 'blur_linear'
order = 0
header = 'Test app'

table = Table('Videos', headers = ['Video', 'Duration',  'Links'],rows = [
    ['opt_sync1_3_0.mp4', '30 seconds',  '@Refererence 1'],
    ['opt_sync1_3_0.mp4', '37 seconds',  '@Refererence 8']    
], value = 0)

def clean_table(_, value):
    table.rows = []
    return table

clean_button = Button('Clean table', changed = clean_table)

selector = Select('Select', value='All', options=['All','Based','Group'])

list_refs = Select('Detail ref list', type = 'list', options = ['Select reference'])

def dispatch1(_, ref):
    list_refs.options = [f'#{i} {ref}' for i in range(10)]
    return list_refs


@handle(selector,'changed')
def selchanged(_, val):
    if val == 'Based':
        return UpdateError(_,'Select can not be Based!')
    _.value = val    

block = Block('X Block',
    [           
        clean_button,
        selector,
    ], [table, list_refs], Image('logo', fn2url('assets/images/unigui.png'), lambda _,v: Info(f'{v} logo selected!')
), dispatch = dispatch1)

blocks= [block,tblock]
