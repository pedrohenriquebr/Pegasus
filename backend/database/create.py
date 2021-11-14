import json
import pandas as pd
import os
import gspread
from database import dbconnection
from database import schema

db = dbconnection.DbConnection()

 # CREATE A SPREADSHEET
try:
    sheet = db.client.open(dbconnection.SPREADSHEET_NAME)
    print('Spreadsheet {} already exists.'.format(dbconnection.SPREADSHEET_NAME))
    exit(0)
except gspread.exceptions.SpreadsheetNotFound:
    print("Spreadsheet not found")
    print("Creating the spreadsheet")
    sheet = db.client.create(dbconnection.SPREADSHEET_NAME)
except Exception as e:
    print(e)
    exit(1)
sheet.share(dbconnection.USER_EMAIL, perm_type='user', role='owner')

# CREATE A WORKSHEETS
initial_data  = json.load(open(os.path.join(os.sep,os.path.dirname(__file__),'initial_data\initial_data.json'), encoding='utf-8'))
schema  = schema.schema
for table_name in schema:
    try: 
        worksheet = sheet.worksheet(table_name)
    except:
        print("Worksheet not found")
        print(f'Creating the {table_name} worksheet')
        sheet.add_worksheet(title=table_name, rows="600", cols=schema[table_name].shape[1])
        worksheet = sheet.worksheet(table_name)
    if table_name in initial_data.keys():
        schema[table_name] = schema[table_name].append(pd.DataFrame(initial_data[table_name], columns=schema[table_name].columns)).fillna('null')
        worksheet.update([schema[table_name].columns.values.tolist()] + schema[table_name].values.tolist())
print("Spreadsheet created")