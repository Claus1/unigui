from unigui import *
from blocks.tblock import config_area
user = get_user()

name = "Main"
icon = 'blur_linear'
order = 0
header = 'Test app'

table = Table('Videos', 0, headers = ['Video', 'Duration',  'Links'],rows = [
    ['opt_sync1_3_0.mp4', '30 seconds',  '@Refer to signal1'],
    ['opt_sync1_3_0.mp4', '37 seconds',  '@Refer to signal8']    
])

def clean_table(_, value):
    table.rows = []
    return table

clean_button = Button('Clean table', clean_table)

selector = Select('Select', 'All', options=['All','Based','Group'])

list_refs = Select('Detail ref list signals', type = 'list', options = ['Select reference'])

def block_dispatch(_, ref):
    list_refs.options = [f'#{i} {ref}' for i in range(10)]
    return list_refs


@handle(selector,'changed')
def selchanged(_, val):
    if val == 'Based':
        return UpdateError(_,'Select can not be Based!')
    _.value = val    

image = Image('logo', fn2url('images/unigui.png'), lambda _,v: Info(f'{v} logo selected!'))

def replace_image(_, iname):
    print(iname)
    image.image = fn2url(f'images/{iname}')
    return image

block = Block('X Block',
    [           
        clean_button,
        selector,
    ], [table, list_refs], icon = 'api')
bottom_block = Block('Bottom block', 
    [
        Button('Replace the logo', replace_image, type = 'gallery'),
        Button('Happy signal', lambda _, v: Signal(_, 'make everyone happy'))
    ],
     image, 
    dispatch = block_dispatch)

blocks= [[block,bottom_block],config_area]
