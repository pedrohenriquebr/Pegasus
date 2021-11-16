from typing import TypeVar
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd

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
        return self.sheet
    
    def share(self, user_email: str, perm_type: str = 'user', role: str = 'writer'):
        self.sheet.share(user_email, perm_type, role)
    
    def get_repository(self,T ) -> Repository[T]:
        return Repository[T](self.sheet.worksheet(T.__dict__['__model']['__worksheet_name']),T.__dict__['__model'])
    
    def upsert(self,name: str, dataframe: pd.DataFrame):
        df = dataframe.copy()
        for x in  df.select_dtypes(include=['datetime64','datetime64[ns]','<M8[ns]']).columns.tolist():
            df[x] = df[x].dt.strftime('%Y-%m-%d %H:%M:%S %z')
        self.sheet.worksheet(name).update([df.columns.values.tolist()] + df.fillna('null').values.tolist())

