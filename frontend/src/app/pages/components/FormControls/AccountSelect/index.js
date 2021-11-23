import { useState,useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import api from './../../../../services/api';

import Form from 'react-bootstrap/Form';
export default function AccountSelect({onAccountChange}) {
    const [account, setAccount] = useState('');
    const [accounts, setAccounts] = useState([]);
    const { t } = useTranslation();

    useEffect(() => {
        api.get('/accounts/autocomplete',).then(d => {
            setAccounts(d.data.data.map(d=> ({text: d.name, value:d.id})));
        })
    }, [])
    
    const handleChange = (event) => {
        setAccount(event.target.value);
       if(onAccountChange) onAccountChange(event.target.value);
    };
    return (
        <Form.Select aria-label="Default select example" onChange={handleChange}>
            <option value="0">{t('labels.account')}</option>
            {accounts.map((account, index) => (
                <option key={index} value={account.value}>{account.text}</option>
            ))}
        </Form.Select>
    )
}