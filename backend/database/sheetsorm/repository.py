from typing import Callable, Generic, List, TypeVar
from collections import namedtuple
import datetime
import gspread
import pandas as pd
from pandas.core.frame import DataFrame
from .util import DTYPES


T  = TypeVar('T')
nullable_values = {
    'str': '',
    'int': 0,
    'float': 0.0,
    'bool': False,
    'date': None,
    'datetime': None,
    'time': None,

}
class Repository(Generic[T]):
    def __init__(self, worksheet: gspread.models.Worksheet, model):
        self.worksheet  = worksheet
        self.model = model
        self.pending = []
        self.primary_key  = [x['attribute'] for x in self.model['__data'] if x['primary_key'] == True][0]
        self.name_to_attribute = {x['name']: x['attribute'] for x in self.model['__data']}
        self.attribute_to_name = {x['attribute']: x['name'] for x in self.model['__data']}
        
    
    def get_attribute_by_name(self, attr,value):
        

        if value == '' or value == 'null' or value == None:
            return nullable_values[attr['dtype']]

        if attr['dtype'] == 'int':
            return 0 if value =='null' else int(value)
        elif attr['dtype'] == 'str':
            # get the lenthg of the varchar
            length = attr['length'] if attr['length'] != None else 200
            value = str(value)
            if len(value) > int(length):
                Exception('Value is too long')
            return value[0: int(length)]
        elif attr['dtype'] == 'datetime':
            value = str(value)
            return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        elif attr['dtype'] == 'bool':
            return bool(value == '1' or value == 'True')    
        elif attr['dtype'] == 'float':
            return float(value)
        else:
            raise Exception('Unsupported type -> ', attr['dtype'], f'"{value}"')
    

    def to_dataframe(self) -> pd.DataFrame:
        temp_df  = DataFrame({
            column['name']: pd.Series(dtype=DTYPES[column['dtype']]) for column  in self.model['__data']
        })

        temp_df = temp_df.append(pd.DataFrame(self.worksheet.get_all_records()))
        temp_df = temp_df.applymap(lambda x: None if x in ['null',''] else x)
        for column in temp_df.columns:
             if temp_df[column].dtype == 'datetime64[ns]':
                temp_df[column] = pd.to_datetime(temp_df[column])
            else:
                temp_df[column] = temp_df[column].astype(temp_df[column].dtype)
        return temp_df

    def get_builtin(name) :
        return getattr(__builtins__, name)

    def _sheet_row_to_object(self, row: dict):
        obj = None
        obj = namedtuple(self.worksheet.title, ' '.join([x['attribute'] for x in self.model['__data']]))
        # "<Table(id='%d', name='%s')>"
        # dinamic namedtuple
        for attr in self.model['__data']:
            setattr(obj,attr['attribute'],self.get_attribute_by_name(attr,row[attr['name']]))
        return obj
    
    def _object_to_dict(self, obj: T, primary_key = False) -> dict:
        return {attr['name']: getattr(obj, attr['attribute']) for attr in self.model['__data'] if primary_key and  attr['primary_key'] or not attr['primary_key']}
    
    def get_all(self) -> List[T]:
        return [self._sheet_row_to_object(row) for row in  self.worksheet.get_all_records()]

    def add(self, obj: T):
        self.pending.append({'operation': 'add', 'obj': obj})
    
    def remove(self, obj: T):
        self.pending.append({'operation':'delete', 'obj':obj})
    
    def update(self, obj: T):
        # check if the object is in the pending updates
        search = [getattr(x['obj'], self.primary_key) == getattr(obj, self.primary_key) for x in self.pending]
        if not any(search):
            self.pending.append({'operation':'update', 'obj': obj})
        else:
            # update the object
            self.pending[search.index(True)] = {'operation':'update', 'obj': obj}

    def find(self, call: Callable):
        df = self.get_all()
        return [x for x in df if call(x)]
    
    def any(self, call: Callable):
        return any(call(x) for x in self.get_all())
    
    def all(self, call: Callable):
        return all(call(x) for x in self.get_all())
    
    def count(self, call: Callable):
        return len([x for x in self.get_all() if call(x)])
    
    
    def commit(self):
        # load the dataframe
        df = self.to_dataframe()
        primary_key = self.primary_key

        for operation in self.pending:
            obj  = operation['obj']
            if operation['operation'] == 'add':
                if getattr(obj,primary_key) == None:
                    raise Exception('Primary key is not set')
                # check if the primary key already exists
                if df[primary_key].isin([getattr(obj,primary_key)]).any():
                    raise Exception('Primary key already exists')
                # get the name of the columns
                new_dict = self._object_to_dict(obj)
                # add the row
                df = df.append(new_dict, ignore_index=True)
            elif operation['operation'] == 'delete':
                # get the name of the columns
                primary_key_value = getattr(obj,primary_key)
                # remove the row
                df = df[df[primary_key] != primary_key_value]
            elif operation['operation'] == 'update':
               # check the primary key
                if getattr(obj,primary_key) == None:
                    raise Exception('Primary key is not set')
                # check if the primary key if not exists
                if not df[primary_key].isin([getattr(obj,primary_key)]).any():
                    raise Exception('Primary key does not exists')
                
                # get the name of the columns
                new_dict = self._object_to_dict(obj,primary_key=True)
                # update the row
                df.loc[df[primary_key] == getattr(obj,primary_key), new_dict.keys()] = new_dict.values()
            else:
                raise Exception('Unsupported operation -> ', operation['operation'])
        # save the dataframe

        self._df_copy = df.copy()
        self._df_copy = self._df_copy.fillna('null')
        for x in  self._df_copy.select_dtypes(include=['datetime64','datetime64[ns]','<M8[ns]']).columns.tolist():
            self._df_copy[x] = self._df_copy[x].apply(lambda x: x.dt.strftime('%Y-%m-%d %H:%M:%S'))
            self._df_copy[x] = self._df_copy[x].astype(str)
        self.worksheet.update([self._df_copy.columns.values.tolist()] + self._df_copy.values.tolist())
        
