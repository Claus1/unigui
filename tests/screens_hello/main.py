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


select_concept_mode = Select('Select', value='All', options=['All','Based','Group'])
select_concept_group = Select('Group', value='Group 1', options=['Group 1','Group 2', 'Group 3'])

def clean_table(_, value):
    table.rows = []
    return table

clean_button = Button('Clean table', changed = clean_table)

block = Block('X Block', 
    [           
        clean_button,
        select_concept_mode,
        select_concept_group,
    ], table)

blocks= [block,tblock]
