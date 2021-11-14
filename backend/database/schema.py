import pandas as pd

schema = {
    'TBL_AccountGroup': pd.DataFrame({
        'ID_AccountGroup': pd.Series(dtype='int'),
        'DS_Name': pd.Series(dtype='str'),
    }),
    'TBL_Account': pd.DataFrame({
        'ID_Account': pd.Series(dtype='int'),
        'ID_AccountGroup': pd.Series(dtype='int'),
        'DT_CreatedDate': pd.Series(dtype='datetime64[ns]'),
        'NR_InitialAmount': pd.Series(dtype='float'),
        'DS_Name': pd.Series(dtype='str'),
        'NR_Number': pd.Series(dtype='str'),
        'DS_BankOfficeNumber': pd.Series(dtype='str'),
        'DS_Bank': pd.Series(dtype='str')
    }),
    'TBL_Category': pd.DataFrame({
        'ID_Category': pd.Series(dtype='int'),
        'ID_CategoryParent': pd.Series(dtype='int'),
        'DS_Name': pd.Series(dtype='str'),
        'NR_Level': pd.Series(dtype='int')
    }), 
    'TBL_Transactions': pd.DataFrame({
        'ID_Transaction': pd.Series(dtype='int'),
        'ID_Account': pd.Series(dtype='int'),
        'ID_AccountDestination': pd.Series(dtype='int'),
        'CD_Type': pd.Series(dtype='str'),
        'ID_Category': pd.Series(dtype='int'),
        'DT_TransactionDate': pd.Series(dtype='datetime64[ns]'),
        'DT_RegistrationDate': pd.Series(dtype='datetime64[ns]'),
        'NR_Amount': pd.Series(dtype='float'),
        'IC_Imported': pd.Series(dtype='bool'),
        'DS_Description': pd.Series(dtype='str'),
        'DS_AttachmentDetails': pd.Series(dtype='str'),
        'DS_AttachmentPath': pd.Series(dtype='str'),
        'DT_ImportedDate': pd.Series(dtype='datetime64[ns]'),
        'NR_Balance': pd.Series(dtype='float')
    }),
    'TBL_DescriptionCategory': pd.DataFrame({
        'DS_Description': pd.Series(dtype='str'),
        'ID_Category': pd.Series(dtype='int')
    }), 
    'DIM_DT_TransactionDate': pd.DataFrame({
        'ID_TransactionDate': pd.Series(dtype='int'),
        'DT_TransactionDate': pd.Series(dtype='datetime64[ns]')
    }),
    'DIM_DS_Description': pd.DataFrame({
        'ID_DS_Description': pd.Series(dtype='int'),
        'DS_Description': pd.Series(dtype='str')
    }),
    'DIM_NR_Income': pd.DataFrame({
        'ID_Income': pd.Series(dtype='int'),
        'NR_Value': pd.Series(dtype='float')
    }),
    'DIM_NR_Expense': pd.DataFrame({
        'ID_Expense': pd.Series(dtype='int'),
        'NR_Value': pd.Series(dtype='float')
    }),
    'DIM_NR_Balance': pd.DataFrame({
        'ID_Balance': pd.Series(dtype='int'),
        'NR_Balance': pd.Series(dtype='float')
    }),
    'DIM_Transfers': pd.DataFrame({
        'ID_Transfer': pd.Series(dtype='int'),
        'NM_Origin': pd.Series(dtype='str'),
        'NM_Destination': pd.Series(dtype='str'),
        'NR_Value': pd.Series(dtype='float')
    }),
    'FAT_Transactions': pd.DataFrame({
        'ID_Transaction': pd.Series(dtype='int'),
        'ID_TransactionDate': pd.Series(dtype='int'),
        'ID_DS_Description': pd.Series(dtype='int'),
        'ID_Income': pd.Series(dtype='int'),
        'ID_Expense': pd.Series(dtype='int'),
        'ID_Balance': pd.Series(dtype='int'),
        'ID_Transfer': pd.Series(dtype='int')
    }),
    'DW_Base': pd.DataFrame({
        'ID_Base': pd.Series(dtype='int'),
        'ID_Account': pd.Series(dtype='int'),
        'DT_TransactionDate': pd.Series(dtype='datetime64[ns]'),
        'DS_Description': pd.Series(dtype='str'),
        'NR_Value': pd.Series(dtype='float'),
        'NR_Balance': pd.Series(dtype='float')
    })
}
