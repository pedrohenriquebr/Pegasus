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
        if type(value).__name__ != column['dtype']:
            raise TypeError(f"{column['attribute']} must be of type '{column['dtype']}'")
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
        @column
        def ID_Test(self) -> int:
            pass
        
    obj = Test()
    obj.ID_Test = 1
    print(obj.ID_Test)
    ```
    """

    def inner_model(func):
        data = []
        _columns = dict(func.__dict__)
        original_dict = {x: v for x,v in  _columns.items() if str(type(v)) == "<class 'function'>" and '__column__' in v.__dict__}
            
        for m in original_dict:
            column : Column = original_dict[m].__column__
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



        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.__model = {
            '__data' : data,
            '__worksheet_name' : worksheet if worksheet != None else func.__name__
        }
        
        
        return wrapper
    return inner_model

def column(name:str='',dtype:str='', length:int=200,primary_key:bool=False,auto_increment=True):
    def inner_column(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        
        wrapper.__column__  = {
            # the name to be used to access the column
            'attribute': func.__name__,
            # the name of the column in the worksheet
            'name': func.__name__ if name == '' else name,
            # the data type of the column
            'dtype': dtype if dtype != '' else func.__annotations__['return'].__name__,
            # the length of the column
            'length': length,
            # if the column is a primary key
            'primary_key': primary_key,
            # if the column is auto increment
            'auto_increment': auto_increment
        }
        return wrapper
    return inner_column

