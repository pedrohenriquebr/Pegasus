from database.entities import TBL_Transactions,TBL_Account,TBL_AccountGroup,TBL_Category
from database.sheetsorm.orm import SheetsORM 


class Uof:
    def __init__(self, db: SheetsORM):
        self.db = db
        self._TransactionsRepository = None
        self._AccountRepository = None
        self._CategoryRepository = None
        self._AccountGroupRepository = None
    
    @property
    def TransactionsRepository(self):
        if self._TransactionsRepository is None:
            self._TransactionsRepository = self.db.get_repository(TBL_Transactions)
        return self._TransactionsRepository

    @property
    def AccountRepository(self):
        if self._AccountRepository is None:
            self._AccountRepository = self.db.get_repository(TBL_Account)
        return self._AccountRepository

    @property
    def AccountGroupRepository(self):
        if self._AccountGroupRepository is None:
            self._AccountGroupRepository = self.db.get_repository(TBL_AccountGroup)
        return self._AccountGroupRepository
    
    @property
    def CategoryRepository(self):
        if self._CategoryRepository is None:
            self._CategoryRepository = self.db.get_repository(TBL_Category)
        return self._CategoryRepository    
    