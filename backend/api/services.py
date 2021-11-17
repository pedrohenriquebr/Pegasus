from typing import List
from api.uof import Uof
from database.sheetsorm.orm import SheetsORM
from database.entities import TBL_Transactions,TBL_Account,TBL_AccountGroup,TBL_Category
from helpers.date import DEFAULT_DATE_FORMAT

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