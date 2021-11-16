from typing import TypeVar
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd

from .util import DTYPES

from .repository import Repository

T  = TypeVar('T')


class SheetsORM:
    def __init__(self, credentials_file: str = None, spreadsheet_name: str = None, scope: list = None):
        """
        SheetsORM constructor

        ### Parameters
        credentials_file: str = None - path to the credentials file
        spreadsheet_name: str = None - name of the spreadsheet
        scope: list = None - list of scopes to use


        ### Raise
        ValueError: if credentials_file is None
        ValueError: if spreadsheet_name is None
        ValueError: if scope is None

        
        """
        if credentials_file is None:
           raise ValueError("credentials_file is None")
        if scope is None:
            raise ValueError("Scope is not defined")
        if spreadsheet_name is None:
            raise ValueError("Spreadsheet name is not defined")
        self.spreadsheet_name = spreadsheet_name
        self.scope = scope
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, self.scope)
        self.client = gspread.authorize(self.creds)
    
    def connect(self,create_if_not_exist: bool = True):
        try:
            self.sheet = self.client.open(self.spreadsheet_name)
        except gspread.exceptions.SpreadsheetNotFound:
            if not create_if_not_exist:
                raise ValueError("Spreadsheet not found")
            else:
                self.sheet = self.client.create(self.spreadsheet_name)
                # self.sheet.share(user_email, perm_type, role)
        return self.sheet
    
    def share(self, user_email: str, perm_type: str = 'user', role: str = 'writer'):
        self.sheet.share(user_email, perm_type, role)
    
    def create_worksheet(self, T):
        schema = T.__dict__['__model']['__schema']
        self.sheet.add_worksheet(title=T.__dict__['__model']['__worksheet_name'], rows="600", cols=schema.shape[1])
        self.upsert(T.__dict__['__model']['__worksheet_name'],schema)
        
    def get_dataframe_schema(self, T):
        return  pd.DataFrame({
            column['name']: pd.Series(dtype=DTYPES[column['dtype']]) for column  in T.__dict__['__model']['__data']})

    def get_repository(self,T ) -> Repository[T]:
        _worksheet_name = T.__dict__['__model']['__worksheet_name']
        try:
            _ws = self.sheet.worksheet(_worksheet_name)
        except gspread.exceptions.WorksheetNotFound:
            df_schema  = self.get_dataframe_schema(T)
            self.sheet.add_worksheet(title=_worksheet_name, rows="600", cols=df_schema.shape[1])
            _ws = self.sheet.worksheet(_worksheet_name)
            _ws.update([df_schema.columns.values.tolist()] + df_schema.values.tolist())
        return Repository[T](_ws,T.__dict__['__model'])
    
    def upsert(self,name: str, dataframe: pd.DataFrame):
        df = dataframe.copy()
        for x in  df.select_dtypes(include=['datetime64','datetime64[ns]','<M8[ns]']).columns.tolist():
            df[x] = df[x].dt.strftime('%Y-%m-%d %H:%M:%S %z')
        self.sheet.worksheet(name).update([df.columns.values.tolist()] + df.fillna('null').values.tolist())

