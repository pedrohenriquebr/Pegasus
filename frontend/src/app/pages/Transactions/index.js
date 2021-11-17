import { useTranslation } from 'react-i18next';
import { AddButton, DeleteButton, EditButton, RefreshButton } from '../components/Buttons';
import AccountSelect from '../components/FormControls/AccountSelect';
import TransactionsGrid from '../components/TransactionsGrid';

export default function TransactionPage() {
    const { t } = useTranslation();
    return (<>
        <h1>{t('transactions.title')}</h1>
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <AccountSelect />
            <div style={{ paddingTop: '10px' }}>
                <RefreshButton />
                <AddButton />
                <EditButton />
                <DeleteButton />
            </div>
        </div>
        <TransactionsGrid></TransactionsGrid>
    </>
    );
}
