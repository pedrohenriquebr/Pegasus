from database.entities import *
from sheetsorm.orm import SheetsORM 


class Uof:
    def __init__(self, db: SheetsORM):
        self.db = db
        self._TransactionsRepository = None
        self._AccountRepository = None
        self._CategoryRepository = None
        self._AccountGroupRepository = None
        self._DescriptionCategory = None
        self._DwBase = None
    
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
    
    @property
    def DwBaseRepository(self):
        if self._DwBase is None:
            self._DwBase = self.db.get_repository(DW_Base)
        return self._DwBase
    
    @property
    def DescriptionCategoryRepository(self):
        if self._DescriptionCategory is None:
            self._DescriptionCategory = self.db.get_repository(TBL_DescriptionCategory)
        return self._DescriptionCategory
    