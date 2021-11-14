import { useTranslation } from 'react-i18next';


export default function TransactionPage() {
    const { t } = useTranslation();
    return (
        <div>
            <h1>{t('transactions.title')}</h1>
        </div>
    );
}
