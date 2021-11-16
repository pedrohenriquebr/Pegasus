from database.sheetsorm.orm import SheetsORM
from database.entities import TBL_Transactions


class TransactionsService:

    def __init__(self, db: SheetsORM):
        self.db = db
    

    def search_transactions(self, limit):
            return [
                self._format_transaction(row)
                for row in self.db.get_repository(TBL_Transactions).get_all()
            ][:limit]

    def _format_transaction(self, transaction: TBL_Transactions):
        return {
            'id': transaction.ID_Transaction,
            'transaction_date': transaction.DT_TransactionDate.strftime('%Y-%m-%d %H:%M:%S'),
            'transaction_type': transaction.CD_Type,
            'amount': transaction.NR_Amount,
            'description': transaction.DS_Description,
            'category': transaction.ID_Category,
            'id_account': transaction.ID_Account,
        }

    