from typing import  TypedDict



class Column(TypedDict):
    """
    Column is a TypedDict that represents a column in a table.

    It has the following keys:
    - name: the name of the column
    - attribute: the attribute of the column
    - dtype: the type of the column
    - primary_key: whether the column is a primary key
    - length: the length of the column
    """
    attribute : str
    name: str
    dtype : str
    length : int
    primary_key : bool


