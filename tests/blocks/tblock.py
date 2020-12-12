from unigui import *

table = Table('Audios', actions = '+-', headers = ['Audio', 'Duration', 'Owner', 'Status', 'Links'],rows = [
    ['opt_sync1_3_0.mp3', '237 seconds', 'Admin', 'Processed', 'Refererence 8'],
    ['opt_sync1_3_0.mp3', '639 seconds', 'Admin', 'Processed', 'Refererence 10']
], value = -1)


select_concept_mode = Select('Delect', value='All', options=['All','Based','Group'])
select_concept_group = Select('Soup', value='Group 1', options=['Soup 1','Soup 2', 'Soup 3'])

tblock = Block('New block', 
    [           
        select_concept_mode,
        select_concept_group,
    ], table, width = 600)

