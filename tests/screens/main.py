from unigui import *
from blocks.tblock import config_area
user = get_user()

name = "Main"
icon = 'blur_linear'
order = 0
header = 'Test app'

table = Table('Videos', 0, headers = ['Video', 'Duration',  'Links', 'Mine'], tools = False, rows = [
    ['opt_sync1_3_0.mp4', '30 seconds',  '@Refer to signal1', True],
    ['opt_sync1_3_0.mp4', '37 seconds',  '@Refer to signal8', False]    
])

def clean_table(_, value):
    table.rows = []
    return table

clean_button = Button('Clean table', clean_table, icon='swipe')

selector = Select('Select', 'All', options=['All','Based','Group'])

list_refs = Select('Detail ref list signals', type = 'list', options = ['Select reference'])

def block_dispatch(_, ref):
    list_refs.options = [f'#{i} {ref}' for i in range(10)]
    return list_refs

@handle(selector,'changed')
def selchanged(_, val):
    if val == 'Based':
        return Error('Select can not be Based!',_)
    _.value = val    

def replace_image(_, iname):
    print(iname)    

block = Block('X Block',
    [           
        clean_button,
        selector,
    ], [table, list_refs], icon = 'api')

def chtable(_, v):
    table.rows[1][0] = 'changed'
    table.value = 1
    return table

graph = Graph('test graph', width = 400, height = 400, nodes = {
    'node1': { 'name': "Node 1" },
    'node2': { 'name': "Node 2" },
    'node3': { 'name': "Node 3" },
    'node4': { 'name': "Node 4" }
  }, edges = {
    'edge1': { 'source': "node1", 'target': "node2" },
    'edge2': { 'source': "node2", 'target': "node3" },
    'edge3': { 'source': "node3", 'target': "node4" },
  })
    
bottom_block = Block('Bottom block', 
    [        
        Button('Happy signal', lambda _, v: Signal(_, 'make everyone happy')), Button('Change table', chtable)
    ],
    [graph, Video("v1", src = "https://v.redd.it/tno0yjw281o81/DASH_1080.mp4?source=fallback", height = 400 )], 
     dispatch = block_dispatch)

blocks= [[block,bottom_block],config_area]
