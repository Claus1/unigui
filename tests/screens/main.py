from unigui import *
from blocks.tblock import append, config_area, cloned_table_typed
user = get_user()

name = "Main"
icon = 'blur_linear'
order = 0
header = 'Test app'

def append_row(table, value):
    row = [''] * 4
    row[-1] = False
    table.rows.append(row)
    return row #new row

table = Table('Videos', 0, headers = ['Video', 'Duration',  'Links', 'Mine'], rows = [
    ['opt_sync1_3_0.mp4', '30 seconds',  '@Refer to signal1', True],
    ['opt_sync1_3_0.mp4', '37 seconds',  '@Refer to signal8', False]
], append = append_row, delete = delete_table_row)

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
        clean_button
        
    ], [table, cloned_table_typed], icon = 'api')

def add_node(_, v):
    for i in range(1000):
        name = f'node{i}'
        if not [n for n in  graph.nodes if n['id'] == name]:
            graph.nodes.append({'id' : name, 'label' : name})
            graph.edges.append({'id': f'edge{i}', 'source': "node1", 'target': f'node{i}' })
            return graph

def graph_selection(_, val):
    _.value = val
    if 'nodes' in val:        
        return Info(f'Nodes {val["nodes"]}') 
    if 'edges' in val:
        return Info(f"Edges {val['edges']}") 
    

graph = Graph('test graph', {'nodes' : ["node1"], 'edges' : ['edge3']}, graph_selection, 
    width = 400, height = 400, nodes = [
     { 'id' : 'node1', 'label': "Node 1" },
     { 'id' : 'node2', 'label': "Node 2" },
     { 'id' : 'node3', 'label': "Node 3" },
     { 'id' : 'node4', 'label': "Node 4" }
  ], edges = [
     { 'id' : 'edge1', 'source': "node1", 'target': "node2", 'label' : 'extending' },
     { 'id' :'edge2' , 'source': "node2", 'target': "node3" , 'label' : 'extending'},
     { 'id' : 'edge3', 'source': "node3", 'target': "node4" , },
  ])
    
bottom_block = Block('Graph block', 
    [        
        Button('Add new node', add_node)
    ],
    [graph, Video("v1", src = "https://v.redd.it/tno0yjw281o81/DASH_1080.mp4?source=fallback", height = 400 )], 
     dispatch = block_dispatch)

blocks= [[block,bottom_block],config_area]
