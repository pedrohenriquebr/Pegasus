import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

env = load_dotenv()

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
        # CREATE A SPREADSHEET
        try:
            sheet = self.client.open(SPREADSHEET_NAME)
        except:
            print("Spreadsheet not found")
            print("Create the spreadsheet first!")
            exit(0)
        return sheet



        
