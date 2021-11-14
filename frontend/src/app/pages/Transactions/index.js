import { useTranslation } from 'react-i18next';
import { AddButton, DeleteButton, EditButton, RefreshButton } from '../components/Buttons';
import AccountSelect from '../components/FormControls/AccountSelect';
import Container from '@mui/material/Container';

export default function TransactionPage() {
    const { t } = useTranslation();
    return (
        <div>
            <h1>{t('transactions.title')}</h1>
            <div style={{ display: 'flex', justifyContent: 'space-between'}}>
                <AccountSelect />
                <div style={{paddingTop:'10px'}}>
                    <RefreshButton />
                    <AddButton />
                    <EditButton />
                    <DeleteButton />
                </div>
            </div>
        </div>
    );
}
