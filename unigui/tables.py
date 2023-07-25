from .guielements import Gui

def accept_cell_value(table, val):    
    value, position = val
    if not isinstance(value, bool):
        try:
            value = float(value)        
        except ValueError:
            pass
        table.rows[position[0]][position[1]] = value    

def delete_table_row(table, value):
    if table.rows:        
        keyed = len(table.headers) < len(table.rows[0])
        table.value = value   
        if isinstance(value, list):        
            if keyed:
                table.rows = [row for row in table.rows if row[-1] not in value]
            else:
                value.sort(reverse=True)
                for v in value:            
                    del table.rows[v]
            table.value = []
        else:
            if keyed:            
                table.rows = [row for row in table.rows if row[-1] != value]
            else:
                del table.rows[value]  
            table.value = None    

def append_table_row(table, value):
    ''' append has to return new row or error string, val is search string in the table'''
    new_id_row, search = value #new_id_row == rows count
    new_row = [''] * len(table.headers)
    if search:
        new_row[0] = search
    table.rows.append(new_row)
    return new_row

class Table(Gui):
    def __init__(self, *args, panda = None, **kwargs):
        if panda is not None:
            self.mutate(PandaTable(*args, panda=panda, **kwargs))
        else:
            super().__init__(*args, **kwargs)           
            if not hasattr(self,'headers'):
                self.headers = []
            if not hasattr(self,'type'):
                self.type = 'table'
            if not hasattr(self,'value'):
                self.value = None
            if not hasattr(self,'rows'):
                self.rows = []        
            if not hasattr(self,'dense'):
                self.dense = True

        if getattr(self,'edit', True):
            edit_setting = hasattr(self,'modify') or hasattr(self,'delete') or hasattr(self,'append')
            if not edit_setting:                             
                self.delete = delete_table_row             
                self.append = append_table_row             
                self.modify = accept_cell_value             
        
    def selected_list(self):                            
        return [self.value] if self.value != None else [] if type(self.value) == int else self.value   

    def clean(self):
        self.rows = []
        self.value = [] if isinstance(self.value,(tuple, list)) else None
        return self

def delete_panda_row(table, row_num):    
    df = table.__panda__
    if row_num < 0 or row_num >= len(df):
        raise ValueError("Row number is out of range")
    pt = table.__panda__
    pt.drop(index = row_num,  inplace=True)
    pt.reset_index(inplace=True) 
    delete_table_row(table, row_num)    

def accept_panda_cell(table, value_pos):
    value, position = value_pos
    row_num, col_num = position
    table.__panda__.iloc[row_num,col_num] = value
    accept_cell_value(table, value_pos)

def append_panda_row(table, row_num):    
    df = table.__panda__
    new_row = append_table_row(table, row_num)
    df.loc[len(df), df.columns] = new_row
    return new_row    

class PandaTable(Table):
    """ panda = opened panda table"""
    def __init__(self, *args, panda = None, fix_headers = True, **kwargs):
        super().__init__(*args, **kwargs)                
        if panda is None:
            raise Exception('PandaTable has to get panda = pandaTable as an argument.')
        self.headers = panda.columns.tolist()
        if fix_headers:
            self.headers = [header.replace('_',' ') for header in self.headers]        
        self.rows = panda.values.tolist()
        self.__panda__ = panda
        
        if getattr(self,'edit', True):
            edit_setting = hasattr(self,'modify') or hasattr(self,'delete') or hasattr(self,'append')
            if not edit_setting:                             
                self.delete = delete_panda_row        
                self.append = append_panda_row        
                self.modify = accept_panda_cell    
    @property
    def panda(self):
        return getattr(self,'__panda__',None) 
    