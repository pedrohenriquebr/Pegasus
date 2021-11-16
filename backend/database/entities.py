from .sheetsorm.decorators import entity, column
from datetime import datetime

@entity()
class TBL_Category:
    ID_Category = column(int,primary_key=True, increment=True,required=True)
    ID_CategoryParent = column(int)
    DS_Name = column(str(250),required=True)
    NR_Level = column(int)

@entity()
class TBL_Transactions:
     ID_Transaction = column(int,primary_key=True, increment=True,required=True)
     ID_Account = column(int,required=True)
     ID_AccountDestination = column(int)
     CD_Type = column(str(12),required=True)
     ID_Category = column(int)
     DT_TransactionDate =  column(datetime,)
     DT_RegistrationDate = column(datetime)
     NR_Amount = column(float)
     IC_Imported = column(bool,default=False)
     DS_Description = column(str(250),required=True)
     DS_AttachmentDetails = column(str(250))        
     DS_AttachmentPath = column(str(250))
     DT_ImportedDate= column(datetime)
     NR_Balance = column(float)

@entity()
class TBL_Account:
    ID_Account = column(int,primary_key=True, increment=True,required=True)
    ID_AccountGroup = column(int)
    DT_CreatedDate = column(datetime,required=True)
    NR_InitialAmount = column(float)
    DS_Name = column(str(250),required=True)
    NR_Number = column(str(250))
    DS_BankOfficeNumber = column(str(250))
    DS_Bank = column(str(250))

@entity()
class TBL_AccountGroup:
    ID_AccountGroup  = column(int,primary_key=True, increment=True,required=True)
    DS_Name  = column(str(250),required=True)


@entity()
class TBL_DescriptionCategory:
    DS_Description  = column(str(250), required=True)
    ID_Category = column(int,required=True) 

@entity()
class TBL_DescriptionTransfer:
    DS_Description  = column(str(250), required=True)
    ID_Transfer = column(int,required=True)