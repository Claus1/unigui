from unigui import *
from blocks.bl import *
name = "Screen 9"

def callback(_, button_name):
    return Info(button_name)

toolbar = [Button('_Save', lambda x,y : Dialog("Who are you?", callback), icon = 'save')]
table = Edit('Vergo', 'sa')

b = Block('Bl 4789', ed, [table], 
    Edit("Fura", "Value"), Button('XXx'), Select('Select','No', options= ['Yesss', 'No']) )

blocks = [b]

def prepare():
    table.value = 'rrr'






