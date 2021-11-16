import os
from database.sheetsorm.orm import SheetsORM


SPREADSHEET_NAME  = os.getenv('SPREADSHEET_NAME','Pegasus - DEV')
USER_EMAIL = os.getenv('USER_EMAIL', 'pedrohenriquebraga735@gmail.com')


db = SheetsORM(scope=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'],
        credentials_file='database/credentials.json', 
        spreadsheet_name=SPREADSHEET_NAME)

db.connect()