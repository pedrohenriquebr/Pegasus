from database.dbconnection import entity, column

@entity()
class TBL_Category: 
    @column(primary_key=True)
    def ID_Category(self) -> int:
       pass
    
    @column()
    def ID_CategoryParent(self) -> int:
       pass

    @column(length=250)
    def DS_Name(self) -> str:
        pass
    

    @column()
    def NR_Level(self) -> int:
        pass


@entity()
class TBL_Transactions:
    @column(primary_key=True)
    def ID_Transaction(self) -> int:
        pass

    @column()
    def ID_Account(self) -> int:
        pass

    @column()
    def ID_AccountDestination(self) -> int:
        pass

    @column(length=12)
    def CD_Type(self) -> str:
        pass

    @column()
    def ID_Category(self) -> int:
        pass

    @column(dtype='datetime')
    def DT_TransactionDate(self):
        pass

    @column(dtype='datetime')
    def DT_RegistrationDate(self):
        pass

    @column()
    def NR_Amount(self) -> float:
        pass

    @column()
    def IC_Imported(self) -> bool:
        pass

    @column(length=250)
    def DS_Description(self) -> str:
        pass

    @column(length=200)
    def DS_AttachmentDetails(self) -> str:
        pass

    @column(length=200)
    def DS_AttachmentPath(self) -> str:
        pass

    @column(dtype='datetime')
    def DT_ImportedDate(self):
        pass

    @column()
    def NR_Balance(self) -> float:
        pass