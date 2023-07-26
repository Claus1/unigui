from data import table
from unigui import *
name = 'Zoo'
order = 1

zoo_table = Table('Zoo Table', panda = table)

sec_table = Table('Sec table', rows = zoo_table.rows, headers = zoo_table.headers)

blocks = [Block('Csv table', [], zoo_table, sec_table)]

