import { useState, useEffect } from 'react';

import { useTranslation } from 'react-i18next';
import api from '../../../services/api';
import { DataGrid } from '@mui/x-data-grid';


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
        { field: 'id', headerName: 'ID_Transaction', type: 'number', width: 100 },
        { field: 'account', headerName: 'ID_Account', type: 'number', width: 60 },
        { field: 'id_account_destination', headerName: 'ID_AccountDestination', type: 'number', width: 60 },
        { field: 'type', headerName: 'CD_Type', type: 'string', width: 100 },
        { field: 'id_category', headerName: 'Category', type: 'string', width: 60 },
        { field: 'transaction_date', headerName: 'DT_TransactionDate', type: 'string', width: 160 },
        { field: 'registration_date', headerName: 'DT_RegistrationDate', type: 'string', width: 160 },
        { field: 'nr_amount', headerName: 'Amount', type: 'number', width: 60 },
        { field: 'ic_imported', headerName: 'IC_Imported', type: 'boolean', width: 60 },
        { field: 'ds_description', headerName: 'DS_Description', type: 'string', width: 60 },
        { field: 'ds_attachment_details', headerName: 'DS_AttachmentDetails', type: 'string', width: 60 },
        { field: 'ds_attachment_path', headerName: 'AttachmentPath', type: 'string', width: 60 },
        { field: 'imported_date', headerName: 'ImportedDate', type: 'string', width: 60 },
        { field: 'nr_balance', headerName: 'NR_Balance', type: 'number', width: 60 },
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
            <DataGrid 
            rows={dataset} 
            columns={columns} 
            pageSize={10} 
            loading={loading}/>
    </div>
    );

}