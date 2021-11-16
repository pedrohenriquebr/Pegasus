from database.sheetsorm.orm import SheetsORM
from database.entities import TBL_Transactions
from helpers.date import DEFAULT_DATE_FORMAT

class TransactionsService:

    def __init__(self, db: SheetsORM):
        self.db = db
    

    def search_transactions(self, offset=0, limit=100):
        # pagination
        # offset -> page
        # limit -> page size
        data = [self._format_transaction(row) 
            for row in self.db.get_repository(TBL_Transactions).get_all()]
        
        return {
                'count': len(data),
                'page': offset,
                'total_pages': int(len(data)/limit)+1,
                'data': data,
            }

    def _format_transaction(self, transaction: TBL_Transactions):
        return {
            'id': transaction.ID_Transaction,
            'transaction_date': transaction.DT_TransactionDate.strftime(DEFAULT_DATE_FORMAT) if transaction.DT_TransactionDate else '',
            'type': transaction.CD_Type,
            'amount': transaction.NR_Amount,
            'description': transaction.DS_Description,
            'category': transaction.ID_Category,
            'id_account': transaction.ID_Account,
            'id_account_destination': transaction.ID_AccountDestination,
            'is_imported': transaction.IC_Imported,
            'imported_date': transaction.DT_ImportedDate.strftime(DEFAULT_DATE_FORMAT) if transaction.DT_ImportedDate else '',
            'balance': transaction.NR_Balance
        }

    