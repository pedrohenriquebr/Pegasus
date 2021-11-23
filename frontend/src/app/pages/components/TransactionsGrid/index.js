import { useState, useEffect } from 'react';

import { useTranslation } from 'react-i18next';
import api from '../../../services/api';


export default function TransactionsGrid(props) {
    const { t, i18n } = useTranslation();

    // ID_Transaction
    // ID_Account
    // ID_AccountDestination
    // CD_Type
    // ID_Category
    // DT_TransactionDate
    // DT_RegistrationDate
    // NR_Amount
    // IC_Imported
    // DS_Description
    // DS_AttachmentDetails
    // DS_AttachmentPath
    // DT_ImportedDate
    // NR_Balance

    const columns = [
        { field: 'id', headerName: 'ID_Transaction',},
        { field: 'account', headerName: 'ID_Account',},
        { field: 'id_account_destination', headerName: 'ID_AccountDestination',},
        { field: 'type', headerName: 'CD_Type',},
        { field: 'id_category', headerName: 'Category'},
        { field: 'transaction_date', headerName: 'DT_TransactionDate',},
        { field: 'registration_date', headerName: 'DT_RegistrationDate',},
        { field: 'nr_amount', headerName: 'Amount',},
        { field: 'ic_imported', headerName: 'IC_Imported',},
        { field: 'ds_description', headerName: 'DS_Description',},
        { field: 'ds_attachment_details', headerName: 'DS_AttachmentDetails'},
        { field: 'ds_attachment_path', headerName: 'AttachmentPath',},
        { field: 'imported_date', headerName: 'ImportedDate'},
        { field: 'nr_balance', headerName: 'NR_Balance',},
    ];


    const [loading, setLoading] = useState(true);
    const [dataset, setDataset] = useState([]);

    useEffect(() => {
        api.post('/transactions/get-all',{id_account: 1}).then(d => {
            setTimeout(() => {
                setDataset(d.data['data']);
                setLoading(false);
            }, 1000);
        }).catch(e => {
            console.log(e);
        });

    });

    return (
        <div style={{width: '100%', height:300}}>
            {/* <DataGrid 
            rows={dataset} 
            columns={columns} 
            pageSize={10} 
            loading={loading}/> */}
    </div>
    );

}