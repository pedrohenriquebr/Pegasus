import os
from sheetsorm.orm import SheetsORM

SPREADSHEET_NAME  = os.getenv('SPREADSHEET_NAME',None)
USER_EMAIL = os.getenv('USER_EMAIL', None)
CREDENTIALS_FILE_URL = os.getenv('CREDENTIALS_FILE_URL',None)
ENV = os.getenv('ENV','prod')
class Connection:
    @staticmethod
    def get_connection():
        print(f'Connecting to {SPREADSHEET_NAME}')
        print(f'User email: {USER_EMAIL}')
        print(f'Credentials file url: {CREDENTIALS_FILE_URL}')
        print(f'Environment: {ENV}')
        if ENV == 'prod':
            if not SPREADSHEET_NAME:
                raise Exception('SPREADSHEET_NAME is not set')
            if not USER_EMAIL:
                raise Exception('USER_EMAIL is not set')
            if not CREDENTIALS_FILE_URL:
                raise Exception('CREDENTIALS_FILE_URL is not set')
            
        db = SheetsORM(scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'],
        credentials_file='database/credentials.json' if ENV == 'dev' else CREDENTIALS_FILE_URL, 
        is_url=False if ENV == 'dev' else True,
        spreadsheet_name=SPREADSHEET_NAME)
        db.connect()
        return db