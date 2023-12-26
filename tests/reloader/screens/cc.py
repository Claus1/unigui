from unigui import *
from data import *
name = 'Adds'


tree = Tree('_tree', None, options = tree_options)


image = Image(remote_image, width = 300, height = 200)


table = Table('X table', headers = headers, rows = rows, edit = False)


block2 = Block('Table block',[], table)


ptable = Table('P table', panda = panda_table)


block3 = Block('panda', [], ptable)


blocks = [[block3,[ block2, Block('Big',[], tree, image)]]]