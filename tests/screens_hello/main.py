from unigui import *
from blocks.tblock import tblock
user = get_user()

name = "Main"
icon = 'blur_linear'
order = 0
header = 'Test app'

table = Table('Videos', headers = ['Video', 'Duration', 'Owner', 'Status', 'Links'],rows = [
    ['opt_sync1_3_0.mp4', '30 seconds', 'Admin', 'Processed', 'Refererence 1'],
    ['opt_sync1_3_0.mp4', '37 seconds', 'Admin', 'Processed', 'Refererence 8']    
], value = 0)

def clean_table(_, value):
    table.rows = []
    return table

clean_button = Button('Clean table', changed = clean_table)

selector = Select('Select', value='All', options=['All','Based','Group'])

@handle(selector,'changed')
def selchanged(_, val):
    if val == 'Based':
        return UpdateError(_,'Select can not be Based!')
    _.value = val    

block = Block('X Block', 
    [           
        clean_button,
        selector,
    ], table)

blocks= [block,tblock]
