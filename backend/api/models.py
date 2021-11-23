from enum import Enum


from typing import List, NamedTuple, TypedDict


class FilterDict(TypedDict):
    """
    TypedDict for filter
    """
    attribute: str
    filter_name : str
    filter_value: str

class Order(Enum):
    """
    Enum for order
    """
    ASC = 1
    DESC = 2

class SortDict(TypedDict):
    """
    TypedDict for sort
    """
    name: str
    value: Order

class TransactionsSearchCommand():
    """
    A named dictionary for searching transactions.
    """
    offset: int 
    limit: int
    id_account: int 
    sort: List[SortDict] 
    filters: List[FilterDict]


class ImportationCommand(TypedDict):
    """
    TypedDict for importation
    """
    statement_path: str
    bank_name: str
    id_account: int
    skip_rows: int