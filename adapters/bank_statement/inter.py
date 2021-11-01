import pandas as pd
import helpers.currency as currency

def load_statement(statement_path):
    tmp = pd.read_csv(open(statement_path, 'r'),delimiter=';',skiprows=7,
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
    return tmp[['DT_TransactionDate','DS_Description','NR_Value','NR_Balance']]
    