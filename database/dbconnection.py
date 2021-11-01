import os
from typing import Any
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from database.schema  import schema


SPREADSHEET_NAME  = os.getenv('SPREADSHEET_NAME','Pegasus - DEV')
USER_EMAIL = os.getenv('USER_EMAIL')



class DbConnection:
    def __init__(self):
        # define the scope
        self.scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

        # add credentials to the account
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('database/credentials.json', self.scope)
    
        self.client = gspread.authorize(self.creds)
    
    def connect(self,):
        try:
            self.sheet = self.client.open(SPREADSHEET_NAME)
        except:
            print("Spreadsheet not found")
            print("Create the spreadsheet first!")
            exit(0)
        return self.sheet
    
    def worksheet(self, name: str) -> pd.DataFrame:
        return schema[name].append(self.sheet.worksheet(name).get_all_records())



        
