from data import table
from unigui import *
name = 'Zoo'

zoo_table = PandaTable('Zoo Table', panda = table)

blocks = [Block('Csv table', [], zoo_table)]

