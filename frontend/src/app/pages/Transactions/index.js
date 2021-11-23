import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import BootstrapTable from 'react-bootstrap-table-next';

import { useTranslation } from 'react-i18next';
import { AddButton, DeleteButton, EditButton, RefreshButton } from '../components/buttons';
import AccountSelect from '../components/FormControls/AccountSelect';

export default function TransactionPage() {
    const { t } = useTranslation();

    const columns = [
        { dataField: 'id', text: 'ID_Transaction', },
        { dataField: 'account', text: 'ID_Account', },
        { dataField: 'id_account_destination', text: 'ID_AccountDestination', },
        { dataField: 'type', text: 'CD_Type', type: 'string', width: 100 },
        { dataField: 'id_category', text: 'Category', },
        { dataField: 'transaction_date', text: 'DT_TransactionDate', },
        { dataField: 'registration_date', text: 'DT_RegistrationDate', },
        { dataField: 'nr_amount', text: 'Amount', },
        { dataField: 'ic_imported', text: 'IC_Imported', },
        { dataField: 'ds_description', text: 'DS_Description', },
        { dataField: 'ds_attachment_details', text: 'DS_AttachmentDetails',},
        { dataField: 'ds_attachment_path', text: 'AttachmentPath', },
        { dataField: 'imported_date', text: 'ImportedDate', },
        { dataField: 'nr_balance', text: 'NR_Balance', },
    ];


    return (
    <Container>
        <Row>
         <Col>
         <h1>{t('transactions.title')}</h1></Col>
        </Row>
        <Row>
           <Col md={2}>
           <AccountSelect />
           </Col>
            <Col md={{span:3, offset:10}} style={{display:'flex', justifyContent:'space-around'}}>
                <RefreshButton />
                <AddButton />
                <EditButton />
                <DeleteButton />
            </Col>
        </Row>

        <Row>
        <BootstrapTable
            keyField="id"
            data={ [] }
            columns={ columns }
            // defaultSorted={ defaultSorted } 
            />
        </Row>
    </Container>
    );
}
