from functools import wraps
from typing import Callable
from .models import Column

def property_maker(column: Column):
    """
    This function is used to create properties for the model
    ### Parameters
    column: Column -> the column to be created

    Thanks to https://stackoverflow.com/questions/60686572/dynamic-property-getter-and-setter
    """
    storage_name = '_' + column['attribute'].lower()

    @property
    def prop(self):
        return getattr(self, storage_name)

    @prop.setter
    def prop(self, value):
        if  column['required'] and value == None:
            raise ValueError(f"{column['attribute']} must not be null")
        if type(value).__name__ != column['dtype']:
            raise TypeError(f"{column['attribute']} must be of type '{column['dtype']}'")
        if column['dtype'] == 'str' and len(value) > column['length']:
            raise ValueError(f"{column['attribute']} must be less than {column['length']} characters")
        setattr(self, storage_name, value)

    return prop

def entity(worksheet:str=None):
    """
    Make the class an entity.
    ### Parameters
    worksheet: The worksheet name to use, default is the name of class

    Each property of the class will be a column in the worksheet.
    You can use the @column decorator to define the column.
    Then you will be able to access the property as a column in the worksheet.
    
    
    ### Returns
    The class with metadata of an entity

    ### Example
    ```python
    @entity(worksheet='Test')
    class Test:
        ID_Test = column(int,primary_key=True)
        
    obj = Test()
    obj.ID_Test = 1
    print(obj.ID_Test)
    ```
    """

    def inner_model(func):
        data = []
        _columns = dict(func.__dict__)
        original_dict = {x: v for x,v in  _columns.items() if str(type(v)) == "<class 'function'>" and '__column__' in v.__dict__}
        primary_keys = 0
        for m in original_dict:
            column : Column = original_dict[m].__column__
            
            if column['primary_key']:
                primary_keys += 1
            
            if primary_keys > 1:
                raise ValueError("Only one primary key is allowed")
            
            column['attribute'] = m
            column['name']  = column['attribute'] if column['name'] == '' else column['name']
            default_value = None
            storage_name = '_'+m.lower()
            if column['dtype'] == 'int':
                default_value = 0
            elif column['dtype'] == 'float':
                default_value = 0.0
            elif column['dtype'] == 'str':
                default_value = ''
            elif column['dtype'] == 'bool':
                default_value = False
            elif column['dtype'] == 'datetime':
                default_value = None
            elif column['dtype'] == 'date':
                default_value = None
            setattr(func,storage_name,default_value)
            setattr(func,m, property_maker(column))
            data.append(column)
        def __init__wrapper(self,*args, **kwargs):
            for k,v in kwargs.items():
                if k not in original_dict:
                    raise ValueError(f"'{k}' is not a valid column")
                setattr(self,k,v) 
        setattr(func,'__init__',__init__wrapper)




        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args,**kwargs)
        wrapper.__model = {
            '__data' : data,
            '__worksheet_name' : worksheet if worksheet != None else func.__name__
        }
        
        
        return wrapper
    return inner_model

def get_type_name(x):
    return x.__name__ if type(x) != str else type(x).__name__

def column(dtype,name:str='',primary_key:bool=False,increment=False, required=False,default=None):
    def wrapper(*args, **kwargs):
        return ''

    type_name  = get_type_name(dtype)
    wrapper.__column__  = {
        # the name to be used to access the column
        'attribute': '',
        # the name of the column in the worksheet
        'name': name,
        # the data type of the column
        'dtype': type_name,
        # the length of the column
        'length': int(dtype) if type_name == 'str' else 0,
        # if the column is a primary key
        'primary_key': primary_key,
        # if the column is auto increment
        'increment': increment,
        'required': required,
        'default': default
    }
    return wrapper

