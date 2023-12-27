from unigui import *
from blocks.tblock import config_area, tarea

name = "Main"

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

clean_button= Button('Clean table', clean_table, icon='swipe')

selector = Select('Select', 'All', options=['All','Based','Group'])

@handle(selector,'changed')
def selchanged(_, val):
    if val == 'Based':
        return Error('Select can not be Based!',_)
    _.accept(val)    

def replace_image(_, iname):
    print(iname)    

block = Block('X Block',
    [           
        clean_button,
        selector
    ], [tarea, table], icon = 'api')

def add_node(_, v):
    for i in range(1000):
        name = f'node{i}'
        if not [n for n in  graph.nodes if n['id'] == name]:
            graph.nodes.append({'id' : name, 'label' : name})
            graph.edges.append({'id': f'edge{i}', 'source': "node1", 'target': f'node{i}' })
            return graph

def graph_selection(_, val):
    _.value = val    
    return Info(f'Nodes {val["nodes"]}, Edges {val["edges"]}') 
    
graph = Graph('test graph', {'nodes' : [0], 'edges' : [2]}, graph_selection, 
    width = 400, height = 400,  nodes = [
     { 'label': "Node 1" },
     { 'label': "Node 2" },
     { 'label': "Node 3" },
     { 'label': "Node 4" }
  ], edges = [
     { 'source': 0, 'target': 1, 'label' : 'extending' },
     { 'source': 1, 'target': 2 , 'label' : 'extending'},
     { 'source': 2, 'target': 3  },
  ])
remote_image ="https://bestfriends.org/sites/default/files/styles/hero_mobile/public/hero-dash/Asana3808_Dashboard_Standard.jpg?h=ebad9ecf&itok=cWevo33k"

bottom_block = Block('Graph, press Shift for multi (de)select', Button('Add node', add_node),    
    [graph, Image(remote_image, width = 450, height = 400)], 
)

blocks= [[block,bottom_block],config_area]

def log(x,y):    
    for i in range(3):
        user.sync_send(Warning(str(i)))
    
toolbar = [Button('_Save', log, icon = 'save', tooltip = 'Save info'),
        Button('_Ignored', lambda _, x: Info('ignored!'), icon = 'delete_forever', tooltip = 'Ignore info!')]
