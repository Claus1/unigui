from unigui import *
from blocks.tblock import tblock
user = get_user()

name = "Main"
icon = 'blur_linear'
order = 0
header = 'Test app'

table = Table('Videos', actions = '+-', headers = ['Video', 'Duration', 'Owner', 'Status', 'Links'],rows = [
    ['opt_sync1_3_0.mp4', '30 seconds', 'Admin', 'Processed', 'Refererence 1'],
    ['opt_sync1_3_0.mp4', '37 seconds', 'Admin', 'Processed', 'Refererence 8']    
], value = 0)


def clean_table(_, value):
    table.rows = []
    return table

clean_button = Button('Clean table', changed = clean_table)

block = Block('X Block', 
    [           
        clean_button,
        Select('Select', value='All', options=['All','Based','Group']),
    ], table)

blocks= [block,tblock]
