from unigui import *
name = "Screen 6"

def callback(_, button_name):
    return Info(button_name)

toolbar = [Button('_Save', lambda x,y : Dialog("Who are you?", callback), icon = 'save')]
table = Edit('Vats', 'sa')


b = Block('Bl 4', [table], 
    Edit("Furia", "Value"), Button('XXx'), Select('Select','No', options= ['Yesss', 'No']) )

blocks = [b]

def prepare():
    table.value = 'rrr'






