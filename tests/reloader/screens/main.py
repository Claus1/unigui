from unigui import *
name = "Screen 6"

table = Edit('Vats', 'sa')


b = Block('Bl 4', [table], 
    Edit("Furia", "Value"), Button('XXx'), Select('Select','No', options= ['Yesss', 'No']) )

blocks = [b]

def prepare():
    table.value = 'rrr'






