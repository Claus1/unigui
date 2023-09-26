from data import table
from unigui import *
name = 'Zoo'
order = 1

zoo_table = Table('Zoo Table', panda = table)

ext_rows = [row * 2 for row in zoo_table.rows]

sec_table = Table('Sec table', rows = ext_rows, headers = zoo_table.headers*2)

blocks = [Block('Csv table', [],  zoo_table,sec_table)]

