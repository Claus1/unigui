from unigui import *
from blocks.bl import *
from folder.a import i
name = "Screen 9"

def callback(_, button_name):
    return Info(button_name)

toolbar = [Button('_Save', lambda x,y : Dialog("Who are you?", callback), icon = 'save')]
table = Edit('Duration', '22 min')

b = Block('Process', Switch('Active', True), Switch('Busy line', True, type = 'check')) 
    #Edit("Fura", i), Button('XXx'), Select('Select','No', options= ['Yesss', 'No']) )

b1 = Block('Audios+', [Button('Button1'), Button('Button2')],   table) 

fish = ['Eel', 'Salmon', 'Tuna']

actors = ['Chris Evans', 'Robert Downey Jr.', 'Jennifer Lawrence', 'Channing Tatum', 
'George Clooney', 'Johnny Depp', 'Margot Robbie', 'Jared Jonson']
b2 = Block('Selection', Select('Fish',None,options =fish, type = 'radio'), 
    Select('Animal','cat', options = ['dog', 'cat','snake', 'beer'], type = 'select'),
    Select('Actors', 'Johnny Depp', options = actors, type = 'list'))

blocks = [b, b1, b2]








