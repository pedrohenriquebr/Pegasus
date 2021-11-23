import pandas as pd
import helpers.currency as currency
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def load_statement(statement_path, skip_rows=5):
    tmp = pd.read_csv(open(statement_path, 'r', encoding=detect_encoding(statement_path)),delimiter=';',skiprows=skip_rows,
        converters= {
            'VALOR': currency.convert_brl,
            'SALDO': currency.convert_brl,
            'HISTÓRICO': lambda x: x.strip()
        })
    tmp['DATA LANÇAMENTO'] = pd.to_datetime(tmp['DATA LANÇAMENTO'], format='%d/%m/%Y')
    tmp = tmp.rename(columns={'DATA LANÇAMENTO':'DT_TransactionDate',
                                            'HISTÓRICO':'DS_Description', 
                                            'VALOR':'NR_Value', 
                                            'SALDO':'NR_Balance'})
    return tmp[['DT_TransactionDate','DS_Description','NR_Value','NR_Balance']].dropna()
    