import argparse
from database.dbconnection import DbConnection
from pegasus2 import Pegasus
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Processar arquivo csv do Banco Inter')
    parser.add_argument('--filename', type=str, default=None, required=False)
    args = parser.parse_args()
    db = DbConnection()
    db.connect()
    
    pegasus.transform()
    pegasus.export_csv()
    pegasus.export_xlsx()