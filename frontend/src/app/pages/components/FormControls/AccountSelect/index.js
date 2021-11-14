import { useState,useEffect } from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormHelperText from '@mui/material/FormHelperText';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { useTranslation } from 'react-i18next';



export default function AccountSelect({onAccountChange, list}) {
    const [account, setAccount] = useState('');
    const [accounts, setAccounts] = useState([]);
    const { t } = useTranslation();

    useEffect(() => {
        setAccounts(list ? list : [{text:'Conta bancária', value:1}, {text:'Carteira', value:2}]);
    }, [])
    
    const handleChange = (event) => {
        setAccount(event.target.value);
       if(onAccountChange) onAccountChange(event.target.value);
    };
    return (
        <div>
            <FormControl sx={{ m: 1, minWidth: 200 }}>
            <InputLabel id="demo-simple-select-helper-label">{t('labels.account')}</InputLabel>
            <Select
                value={account}
                label={t('labels.account')}
                onChange={handleChange}
            >
                <MenuItem value="0">
                    <em>None</em>
                </MenuItem>
                {accounts.map((account, index) => (
                    <MenuItem key={index} value={account.value}>{account.text}</MenuItem>
                ))}
            </Select>
            </FormControl>
        </div>
    )
}