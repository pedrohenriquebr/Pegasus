from typing import List

from pandas.core.tools.datetimes import to_datetime
from api.uof import Uof
from database.sheetsorm.orm import SheetsORM
from database.entities import TBL_Transactions,TBL_Account,TBL_AccountGroup,TBL_Category,DW_Base
from helpers.date import DEFAULT_DATE_FORMAT
from database.schema import schema
from api.config import *

from openpyxl.worksheet.table import Table
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.styles.colors import Color

import pandas as pd
import numpy as np 

class TransactionsService:

    def __init__(self, uof: Uof):
        self.uof = uof
        self.repo = uof.TransactionsRepository


    def get_all_transactions(self,id_account, page=0, limit=10):
        accounts = self.uof.AccountRepository.get_all()
        categories = self.uof.CategoryRepository.get_all()
        data = [self._format_transaction(row,accounts,categories) for row in self.repo.find(lambda x: x.ID_Account == id_account)]
        return {
            'count': len(data),
            'data': data[page*limit:page*limit+limit]
        }

    def _format_transaction(self, transaction: TBL_Transactions, accounts: List[TBL_Account], categories: List[TBL_Category]):
        category = [c for c in categories if c.ID_Category == transaction.ID_Category]
        account = [a for a in accounts if a.ID_Account == transaction.ID_Account]
        account_destination = [a for a in accounts if a.ID_Account == transaction.ID_AccountDestination]
        return {
            'id': transaction.ID_Transaction,
            'transaction_date': transaction.DT_TransactionDate.strftime(DEFAULT_DATE_FORMAT) if transaction.DT_TransactionDate else '',
            'registration_date': transaction.DT_RegistrationDate.strftime(DEFAULT_DATE_FORMAT) if transaction.DT_RegistrationDate else '',
            'type': transaction.CD_Type,
            'amount': transaction.NR_Amount,
            'description': transaction.DS_Description,
            'category':  category[0].DS_Name if len(category) > 0 else '',
            'account_destination': account_destination[0].DS_Name if len(account_destination) > 0 else '',
            'account': account[0].DS_Name if len(account) > 0 else '',
            'id_category': transaction.ID_Category,
            'id_account': transaction.ID_Account,
            'id_account_destination': transaction.ID_AccountDestination,
            'is_imported': transaction.IC_Imported,
            'imported_date': transaction.DT_ImportedDate.strftime(DEFAULT_DATE_FORMAT) if transaction.DT_ImportedDate else '',
            'balance': transaction.NR_Balance
        }


class AccountsService:
    def __init__(self, uof: Uof):
        self.uof = uof
        self.repo = self.uof.AccountRepository
    
    def get_all_accounts(self,offset=0, limit=100):
        accounts_groups = self.uof.AccountGroupRepository.get_all()
        data = [self._format_account(row, accounts_groups) for row in self.repo.get_all()]
        return {
                'count': len(data),
                'data': data[offset*limit:offset*limit+limit]
            }
    
    def get_all_accounts_names(self):
        data = [{'id': row.ID_Account, 'name': row.DS_Name} for row in self.repo.get_all()]
        return {
            'count': len(data),
            'data': data
        }
    
    def _format_account(self, account: TBL_Account, accounts_groups: list):
        group = [group.ID_AccountGroup == account.ID_AccountGroup for group in accounts_groups]
        return {
            'id': account.ID_Account,
            'name': account.DS_Name,
            'group': ( group[0].DS_Name if group[0].DS_Name else '') if len(group) > 0 else '',
            'created_date': account.DT_CreatedDate.strftime(DEFAULT_DATE_FORMAT) if account.DT_CreatedDate else '',
            'initial_amount': account.NR_InitialAmount,
            'number': account.NR_Number,
            'bankoffice_number': account.NR_BankOfficeNumber,
            'bank': account.DS_Bank
        }


class CategoriesService:
    def __init__(self, uof):
        self.uof = uof 
        self.repo = self.uof.CategoryRepository
    
    def get_all_categories(self,offset=0, limit=100):
        data = [self._format_category(row) for row in self.repo.get_all()]
        return {
                'count': len(data),
                'data': data[offset*limit:offset*limit+limit]
            }
    
    def get_all_categories_names(self):
        categories  = self.repo.get_all()
        data = [self._format_category(row,categories) for row in categories]
        return {
            'count': len(data),
            'data': data
        }
    
    def _format_category(self, category: TBL_Category, categories: List[TBL_Category]):
        cat = [cat for cat in categories if cat.ID_Category == category.ID_CategoryParent ]
        return {
            'id': category.ID_Category,
            'name': category.DS_Name,
            'parent': ( cat[0].DS_Name if cat[0].DS_Name else '') if len(cat) > 0 else '',
            'id_parent': category.ID_CategoryParent if category.ID_CategoryParent else 0,
            'level': category.NR_Level,
        }


class ExportationService:
    def  __init__(self, uof: Uof):
        self.uof = uof
        self.sheets = {
            'base':None,
            'dim_entrada': None,
            'dim_saida':None,
            'dim_historico':None,
            'dim_saldo':None,
            'fat_extrato':None,
            'dim_lancamento':None,
            'dim_historico_categoria':None,
            'dim_categoria':None,
            'report':None,
            'historico': None
        }
        self.excel_name_file = 'output.xlsx' 
        self.excel_file = os.path.abspath(UPLOAD_FOLDER + '/' + self.excel_name_file)
        
    def export_data(self):
        self.load_data()
        self._transform()
        self.export_csv()
        self.export_xlsx()
        return self.excel_name_file

    def apply_extra_styles(self,excel_file: str) -> None:
        # load workbook template.xlsx from current directory
        wb = load_workbook(excel_file)

        ws = wb['report']

        # esconde a primeira coluna
        ws.column_dimensions['A'].hidden = True

        # esconder a primeira linha
        ws.row_dimensions[1].hidden = True

        # esconder a 4ª linha
        ws.row_dimensions[4].hidden = True

        # ajustar fonte dos nomes dos meses
        for row in ws['B2:BV2']:
            for cell in row:
                cell.font = Font(size=20)

        # ajustar fonte e cor de fundo dos numeros das semanas
        for row in ws['C3:BV3']:
            for cell in row:
                # converte string em 
                cell.fill = PatternFill("solid", fgColor=Color(rgb='00305496'))
                cell.font = Font(color="ffffffff", bold=True, size=14)

        # percorre as colunas da sheet
        for col in ws.columns:
            # auto ajusta a largura da coluna
            col_name = get_column_letter(col[0].column)
            if col_name == 'B':
                ws.column_dimensions[col_name].width = 38.57
            else:
                ws.column_dimensions[col_name].auto_size = True

        # alterar zoom da worksheet para 85%
        ws.sheet_view.zoomScale = 85

        # formatar valores para o formato R$ ##,## da célula C5:BJ45
        for row in ws['C5:BV43']:
            for cell in row:
                cell.number_format = 'R$ #,##0.00'
                cell.font = Font(size=14)

        # agrupar linhas
        last_start  = 9
        last_end = 8
        for cell in ws['B9:B47']:
            # verificar se o valor da célula é NoneType
            if cell[0].value is None:
                continue
            if cell[0].value.strip() == 'TOTAL':
                continue
            
            if cell[0].value.strip() in [*self.cat_pais, 'Desconhecido']:
                ws.row_dimensions.group(last_start,last_end, hidden=True)
                last_start  = cell[0].row + 2
                last_end = last_start - 1
            else:
                last_end +=1

        ws.row_dimensions.group(last_start,last_end, hidden=True)

        # congelar a coluna B
        ws.freeze_panes = ws['C2']

        # cor das abas das worksheets
        wb['historico'].sheet_properties.tabColor = '203764'
        wb['report'].sheet_properties.tabColor = '203764'
        ws =  wb['historico']
        for row in ws['A1:B1']:
            row[0].fill = PatternFill("solid", fgColor=Color(rgb='00305496'))
            row[0].font = Font(color="ffffffff", bold=True, size=14)
            row[1].fill = PatternFill("solid", fgColor=Color(rgb='00305496'))
            row[1].font = Font(color="ffffffff", bold=True, size=14)

        wb.save(self.excel_file)
        wb.close()
      
    def export_xlsx(self, ) -> None:
        with pd.ExcelWriter(self.excel_file, mode='w') as writer:
            for name, df in self.sheets.items():
                if name == 'report':
                    self.get_report_styles(df).to_excel(writer,sheet_name=name)
                else:
                    df.to_excel(writer,sheet_name=name,index=False)

            
            for name, df in self.sheets.items():
                if name not in  ['report','historico']:
                    writer.sheets[name].sheet_state = 'hidden'
            print(f'Exporting to {self.excel_file} sheets')
        self.apply_extra_styles(self.excel_file)
   
    def get_report_styles(self,pivot_table):
        # the  Styler object dont apply styles on columns or indexes
        
        styles = {
            'TOTAL': 'background-color: #8EA9DB; color: black; font-weight: bold',
            'NR_Balance': 'font-weight: bold;background-color: white;color:black',
            'RECEITA': 'font-weight: bold;background-color: white;color:black',
            'Desconhecido': 'background-color: #305496; color: white; font-weight: bold'
        }

        return pivot_table.style.apply(lambda value, props='': np.where(pivot_table['CATEGORIA'] == 'TOTAL', props, ''), props=styles['TOTAL'], axis=0)\
            .apply(lambda value, props='': np.where(pivot_table['CATEGORIA'] == 'NR_Balance', props, ''), props=styles['NR_Balance'], axis=0)\
            .apply(lambda value, props='': np.where(pivot_table['CATEGORIA'] == 'RECEITA', props, ''), props=styles['RECEITA'], axis=0)\
            .apply(lambda value, props='': np.where(pivot_table['CATEGORIA'] == 'Desconhecido', props, ''), props=styles['Desconhecido'], axis=0)\
            .apply(lambda value, props='': np.where(pivot_table['CATEGORIA'].isin(self.cat_pais), props, ''), props='background-color: #305496; color:white; font-weight:bold', axis=0)\
            .apply(lambda value, props='': np.where(pivot_table['CATEGORIA'].isin(self.cats), props, ''), props='background-color: white; color:black; font-weight:bold', axis=0)\
            .set_properties(**{'border-color':'Black','border-width':'thin','border-style':'solid'})\
            .apply(self._apply_styles, props='font-size: 14pt', col=('CATEGORIA', '', ''),axis=0)

    def _apply_styles(self, x, col, props):
        return [ props if x.name == col else 'font-size: 11pt' for v in x.index ]
    
    def export_csv(self) -> None:
        if not os.path.exists(CACHE_DIR):    
            os.mkdir(CACHE_DIR)
        print('Export DW')

        for outfile, df in self.sheets.items():
            print(f'Exporting {outfile}.csv')
            df.to_csv(os.path.join(CACHE_DIR, f'{outfile}.csv'),sep=';',index=False, header=True, )
    
    def _find_keys(self,dict_):
        key_list = []
        def recursive(obj, last_parent=None,level=1):
            for key in obj.keys():
                if type(obj[key]) == dict:
                    key_list.append({'cat':key, 'level':level , 'cat_parent': last_parent, 'value': None})
                    recursive(obj[key], last_parent=key,level=level+1)
                else:
                    a = len(obj[key])
                    if a >0:
                        for value in obj[key]:
                            key_list.append({'cat': key,'cat_parent': last_parent, 'level': level, 'value': value })

                    else:
                        key_list.append({'cat': key,'cat_parent': last_parent, 'level': level, 'value': None})
            
        recursive(dict_)
        return sorted(key_list, key=lambda x: x['level'])

    def load_data(self) -> None:
        self.TBL_Category = self.uof.CategoryRepository.to_dataframe()
        self.TBL_DescriptionCategory = self.uof.DescriptionCategoryRepository.to_dataframe()
        self.DIM_NR_Income = schema['DIM_NR_Income']
        self.TBL_Transactions = self.uof.TransactionsRepository.to_dataframe()
        transactions = self.uof.TransactionsRepository.get_all()
        self.base_df = pd.DataFrame({
            'ID_Base': pd.Series(dtype='int',data=list(range(1,len(transactions)))),
            'ID_Account': pd.Series(dtype='int', data=[t.ID_Account for t in transactions]),
            'DT_TransactionDate': pd.Series(dtype='datetime64[ns]',data=[t.DT_TransactionDate for t in transactions]),
            'DS_Description': pd.Series(dtype='str', data=[t.DS_Description for t in transactions]),
            'NR_Value': pd.Series(dtype='float', data=[-t.NR_Amount if t.CD_Type in ['Expense','Transfer'] else t.NR_Amount for t in transactions]),
            'NR_Balance': pd.Series(dtype='float', data=[t.NR_Balance for t in transactions]),
        })
        
        self.base_df['DT_TransactionDate'] = pd.to_datetime(self.base_df['DT_TransactionDate'])
        self.base_df  = self.base_df.sort_values('DT_TransactionDate')
        self.base_df = self.base_df[self.base_df['ID_Account'] == 1]
        self.categorias  = self._load_categories()
        self.historico_df = self._load_historic()
    
    def _transform(self):
        # Dimensions

        # dim_entrada
        self.DIM_NR_Income = self.base_df['NR_Value'].loc[self.base_df['NR_Value'] > 0]
        self.DIM_NR_Income.drop_duplicates(inplace=True)
        self.DIM_NR_Income.reset_index(drop=True,inplace=True)
        self.DIM_NR_Income = self.DIM_NR_Income.to_frame()
        self.DIM_NR_Income['ID_Income'] = self.DIM_NR_Income.index + 1
        self.DIM_NR_Income['ID_Income'] = self.DIM_NR_Income['ID_Income'].astype(np.int64)

        # dim_saida
        self.DIM_NR_Expense = self.base_df['NR_Value'].loc[self.base_df['NR_Value'] < 0]
        self.DIM_NR_Expense.drop_duplicates(inplace=True)
        self.DIM_NR_Expense.reset_index(drop=True,inplace=True)
        self.DIM_NR_Expense = self.DIM_NR_Expense.to_frame()
        self.DIM_NR_Expense['ID_Expense'] = self.DIM_NR_Expense.index + 1
        self.DIM_NR_Expense['ID_Expense'] = self.DIM_NR_Expense['ID_Expense'].astype(np.int64)

        # dim_historico
        self.DIM_DS_Description = self.base_df['DS_Description']
        self.DIM_DS_Description.drop_duplicates(inplace=True)
        self.DIM_DS_Description.reset_index(drop=True,inplace=True)
        self.DIM_DS_Description = self.DIM_DS_Description.to_frame()
        self.DIM_DS_Description['ID_DS_Description'] = self.DIM_DS_Description.index + 1
        self.DIM_DS_Description['ID_DS_Description'] = self.DIM_DS_Description['ID_DS_Description'].astype(np.int64)

        # dim_lancamento
        self.DIM_DT_TransactionDate = self.base_df['DT_TransactionDate']
        self.DIM_DT_TransactionDate.drop_duplicates(inplace=True)
        self.DIM_DT_TransactionDate.reset_index(drop=True,inplace=True)
        self.DIM_DT_TransactionDate = self.DIM_DT_TransactionDate.to_frame()
        self.DIM_DT_TransactionDate['ID_TransactionDate'] = self.DIM_DT_TransactionDate.index + 1
        self.DIM_DT_TransactionDate['ID_TransactionDate'] = self.DIM_DT_TransactionDate['ID_TransactionDate'].astype(np.int64)

        # dim_saldo
        self.DIM_NR_Balance = self.base_df['NR_Balance']
        self.DIM_NR_Balance.drop_duplicates(inplace=True)
        self.DIM_NR_Balance.reset_index(drop=True,inplace=True)
        self.DIM_NR_Balance = self.DIM_NR_Balance.to_frame()
        self.DIM_NR_Balance['ID_Balance'] = self.DIM_NR_Balance.index + 1
        self.DIM_NR_Balance['ID_Balance'] = self.DIM_NR_Balance['ID_Balance'].astype(np.int64)


        self.merged = pd.merge(self.base_df,self.DIM_DT_TransactionDate, how='left',on='DT_TransactionDate')
        self.merged = pd.merge(self.merged,self.DIM_NR_Income, how='left',on='NR_Value')
        self.merged = pd.merge(self.merged,self.DIM_NR_Expense, how='left',on='NR_Value')
        self.merged = pd.merge(self.merged,self.DIM_DS_Description, how='left',on='DS_Description')
        self.merged = pd.merge(self.merged,self.DIM_NR_Balance, how='left',on='NR_Balance')

        # # Remove columns
        self.merged.drop(columns=['DS_Description', 'NR_Value', 'DT_TransactionDate','NR_Balance'], inplace=True,errors='ignore')
        self.DIM_NR_Expense['NR_Value'] = self.DIM_NR_Expense['NR_Value'].abs()


        rows = self._find_keys(self.categorias)

        self.dim_categoria = pd.DataFrame({
            'ID_Category': pd.Series(np.arange(start=1,stop=len(rows)+1), dtype=np.int64),
            'DS_Category': pd.Series([row['cat'] for row in rows], dtype=str),
            # temp
            'DS_CategoryParent': pd.Series([row['cat_parent'] for row in rows], dtype=str),
            # temp
            'DS_Description': pd.Series([row['value']  for row in rows], dtype=str),
            'ID_CategoryParent': pd.Series([], dtype=np.int64),
            'NR_Level': pd.Series([row['level'] for row in rows], dtype=np.int64)
        })

        tmp = self.dim_categoria.merge(self.dim_categoria,how='left',left_on='DS_CategoryParent', right_on='DS_Category')
        self.dim_categoria[['ID_Category','DS_Category','ID_CategoryParent','NR_Level']] = tmp[['ID_Category_x','DS_Category_x','ID_Category_y','NR_Level_x']]
        self.dim_categoria = self.dim_categoria.drop(columns=['DS_CategoryParent','DS_Description'])
        self.dim_categoria.drop_duplicates(inplace=True)
        self.dim_categoria['ID_Category'] = self.dim_categoria['ID_Category'].astype(np.int64)
        self.dim_categoria['ID_CategoryParent'] = self.dim_categoria['ID_CategoryParent'].fillna(0)
        self.dim_categoria['ID_CategoryParent'] = self.dim_categoria['ID_CategoryParent'].astype(np.int64)

        self.dim_historico_categoria = pd.DataFrame([],columns=['ID_DS_Description','ID_Category'])
        
        self.dim_historico_categoria = self.DIM_DS_Description\
                                        .merge(self.historico_df, how='left', on='DS_Description')\
                                        .merge(self.dim_categoria, how='left', left_on='DS_Category',right_on='DS_Category')\
                                        .drop_duplicates(['DS_Description','DS_Category'])[['ID_DS_Description','ID_Category']]
    
        self.dim_historico_categoria = self.dim_historico_categoria[['ID_DS_Description','ID_Category']]
        self.dim_historico_categoria['ID_Category'] = self.dim_historico_categoria['ID_Category'].fillna(0)
        self.dim_historico_categoria['ID_Category'] = self.dim_historico_categoria['ID_Category'].astype(np.int64)
        self.dim_historico_categoria['ID_DS_Description'] = self.dim_historico_categoria['ID_DS_Description'].fillna(0)
        self.dim_historico_categoria['ID_DS_Description'] = self.dim_historico_categoria['ID_DS_Description'].astype(np.int64)

        self.cat_pais = self.dim_categoria[self.dim_categoria['NR_Level'] == 1]['DS_Category'].unique()
        self.cats = self.dim_categoria[self.dim_categoria['NR_Level'] > 1]['DS_Category'].unique()

        self.report = self._build_pivot_table(self.merged)
        self.historico = self.build_historico(self.dim_historico_categoria, self.DIM_DS_Description, self.dim_categoria)
        
        self.sheets = {
            'base':self.base_df,
            'dim_entrada': self.DIM_NR_Income,
            'dim_saida':self.DIM_NR_Expense,
            'dim_historico':self.DIM_DS_Description,
            'dim_saldo':self.DIM_NR_Balance,
            'fat_extrato':self.merged,
            'dim_lancamento':self.DIM_DT_TransactionDate,
            'dim_historico_categoria':self.dim_historico_categoria,
            'dim_categoria':self.dim_categoria,
            'report': self.report,
            'historico': self.historico
        }
       
    def _build_pivot_table(self, fat_table: pd.DataFrame):
        report  = self.build_weekly_report(fat_table)
        init_balance = report['NR_Balance'][0] + report['SAIDA'][0] - report['ENTRADA'][0]
        report = report[['DT_TransactionDate','ANO','MÊS','SEMANA','ENTRADA','SAIDA','CATEGORIA']]\
            .groupby(['DT_TransactionDate','ANO','MÊS','SEMANA','CATEGORIA'])\
            .sum([['ENTRADA','SAIDA']]).reset_index().drop(columns=['DT_TransactionDate'])
        filtro = report
        filtro = pd.merge(filtro, self.dim_categoria, how='left',  left_on='CATEGORIA', right_on='DS_Category')
        filtro = pd.merge(filtro, self.dim_categoria, how='left',  left_on='ID_CategoryParent', right_on='ID_Category')
        filtro['CATEGORIA_PAI'] = filtro['DS_Category_y']
        filtro =  filtro[['ANO', 'MÊS','SEMANA', 'CATEGORIA', 'CATEGORIA_PAI','ENTRADA', 'SAIDA']]
        filtro['NR_Value'] = filtro['ENTRADA'] + filtro['SAIDA']
        filtro['CATEGORIA_PAI']  = filtro['CATEGORIA_PAI'].fillna('Desconhecido')
        pivot_table = pd.pivot_table(filtro, values=['NR_Value'],index=['CATEGORIA_PAI','CATEGORIA'],columns=['MÊS','SEMANA'], aggfunc=(np.sum))

        d = filtro.groupby(['CATEGORIA_PAI','CATEGORIA'],as_index=True).sum().index

        groups =[]
        k = []
        for row in d:
            if row[0] not in groups:
                groups.append(row[0])
                k.append((row[0],row[0]))
                k.append((row[0],'TOTAL'))
            k.append((row[0],row[1]))

        pivot_table = pivot_table.reindex(pd.MultiIndex.from_tuples(k,names=['CATEGORIA_PAI','CATEGORIA']))
        pivot_table = pivot_table.reset_index()

        pivot_table.loc[-1] = ['' , 'RECEITA', *[self.calc_income(report,pivot_table,idx) for idx in range(2,pivot_table.shape[1])]]  
        pivot_table.index = pivot_table.index + 1 
        balance_values = []

        for idx in range(2,pivot_table.shape[1]):
            init_balance = self.calc_balance(init_balance, report,pivot_table,idx)
            balance_values.append(init_balance)

        pivot_table.loc[-1] = ['' , 'SALDO', *balance_values]  
        pivot_table.index = pivot_table.index + 1  
        pivot_table = pivot_table.sort_index()
        total_search = pivot_table[pivot_table['CATEGORIA'] == 'TOTAL'] 
        rows =  total_search.iterrows()

        series  = []
        for row in rows:
            cat  = row[1][0]
            label  = row[1][1]
            values = []
            for idx in range(2,pivot_table.shape[1]):
                month, week = pivot_table.columns[idx][1], pivot_table.columns[idx][2]
                values = [*values, filtro[(filtro['MÊS'] == month ) & (filtro['SEMANA'] == week ) & (filtro['CATEGORIA_PAI'] == cat)]['NR_Value'].sum()]
            series.append([cat, label, *values])

        pivot_table[pivot_table['CATEGORIA'] == 'TOTAL']  = pd.DataFrame(series, columns=total_search.columns, index=total_search.index)
        pivot_table = pivot_table.drop(columns=['CATEGORIA_PAI'])
        return pivot_table 
    
    def build_historico(self, dim_historico_categoria: pd.DataFrame, dim_historico: pd.DataFrame, dim_categoria: pd.DataFrame):
        return dim_historico_categoria\
                    .merge(dim_historico,how='left')\
                    .merge(dim_categoria, how='left')\
                    .rename(columns={'DS_Category': 'CATEGORIA'})[['DS_Description','CATEGORIA']]\
                    .fillna('desconhecido')\
                    .drop_duplicates(['DS_Description','CATEGORIA'])
    
    def calc_income(self, report, pivot_table: pd.DataFrame, idx: int):
        # MÊS , SEMANA 
        month, week = pivot_table.columns[idx][1], pivot_table.columns[idx][2]
        temp2  = report[(report['MÊS'] == month) & (report['SEMANA'] == week)]
        return temp2['ENTRADA'].sum()

    def calc_balance(self, init_balance, origin_report, pivot_table: pd.DataFrame, idx: int):
        # MÊS , SEMANA 
        month, week = pivot_table.columns[idx][1], pivot_table.columns[idx][2]

        temp2  = origin_report[(origin_report['MÊS'] == month) & (origin_report['SEMANA'] == week)]
        receitas = temp2['ENTRADA'].sum()
        despesas = temp2['SAIDA'].sum()
        return init_balance + receitas - despesas
   
    def build_weekly_report(self,fat_table: pd.DataFrame):
        report = fat_table.merge(self.DIM_DS_Description, how='left')\
                .merge(self.dim_historico_categoria, how='left')\
                .merge(self.dim_categoria, how='left')\
                .merge(self.DIM_NR_Balance, how='left')\
                .merge(self.DIM_NR_Income, how='left')\
                    .rename(columns={'NR_Value':'ENTRADA'})\
                .merge(self.DIM_NR_Expense, how='left')\
                    .rename(columns={'NR_Value':'SAIDA'})\
                .merge(self.DIM_DT_TransactionDate, how='left')\
                .sort_values(by=['DT_TransactionDate'])

        report[['ENTRADA','SAIDA']] = report[['ENTRADA','SAIDA']].fillna(0)
        report['MÊS'] = report['DT_TransactionDate'].apply(lambda d: MESES[d.month])
        report['MÊS'] = pd.Categorical(report['MÊS'], MESES.values())
        report['ANO'] = report['DT_TransactionDate'].dt.year
        report['SEMANA'] = self._calc_week(report['DT_TransactionDate'])
        report['CATEGORIA'] = report['DS_Category'].fillna('desconhecido')
        return report
    
    def _calc_week(self, series: pd.Series) -> pd.Series:
        first_week = (series - pd.to_timedelta(series.dt.day - 1, unit='d')).dt.weekday
        return (series.dt.day - 1 + first_week) // 7 + 1

    def _load_categories(self,) -> dict:
        categorias = {}
        for row in self.TBL_Category.merge(self.TBL_Category, left_on='ID_CategoryParent',right_on='ID_Category')[['DS_Name_x','NR_Level_x','DS_Name_y']].sort_values('NR_Level_x').to_dict('records'):
            parent  = row['DS_Name_y']
            child   = row['DS_Name_x']
            if parent not in categorias:
                categorias[parent] = {}
            categorias[parent][child] = []
        return categorias

    def _load_historic(self,) -> pd.DataFrame:
        return self.TBL_DescriptionCategory.merge(self.TBL_Category)\
                        .rename(columns={'DS_Name': 'DS_Category'})[['DS_Description','DS_Category']]