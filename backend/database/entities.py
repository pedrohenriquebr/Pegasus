from sheetsorm.decorators import entity, column
from datetime import datetime

@entity()
class TBL_Category:
    ID_Category = column(int,primary_key=True)
    ID_CategoryParent = column(int)
    DS_Name = column(str(250))
    NR_Level = column(int)

@entity()
class TBL_Transactions:
     ID_Transaction = column(int,primary_key=True)
     ID_Account = column(int)
     ID_AccountDestination = column(int)
     CD_Type = column(str(12))
     ID_Category = column(int)
     DT_TransactionDate =  column(datetime)
     DT_RegistrationDate = column(datetime)
     NR_Amount = column(float)
     IC_Imported = column(bool)
     DS_Description = column(str(250))
     DS_AttachmentDetails = column(str(250))        
     DS_AttachmentPath = column(str(250))
     DT_ImportedDate= column(datetime)
     NR_Balance = column(float)

@entity()
class TBL_Account:
    ID_Account = column(int,primary_key=True)
    ID_AccountGroup = column(int)
    DT_CreatedDate = column(datetime)
    NR_InitialAmount = column(float)
    DS_Name = column(str(250))
    NR_Number = column(str(250))
    DS_BankOfficeNumber = column(str(250))
    DS_Bank = column(str(250))