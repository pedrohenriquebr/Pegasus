import { useEffect, useState } from 'react';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';


import { useTranslation } from 'react-i18next';
import { AddButton, DeleteButton, EditButton, RefreshButton } from '../components/buttons';
import AccountSelect from '../components/formcontrols/AccountSelect';
import Grid from '../components/Grid';


export default function TransactionPage() {
    const { t } = useTranslation();
    const [accountId, setAccountId] = useState(1);
    return (
        <Container expand="lg">
            <Row>
                <Col>
                    <h1>{t('transactions.title')}</h1></Col>
            </Row>
            <Row>
                <Col md={2}>
                    <AccountSelect onAccountChange={d => setAccountId(d)} />
                </Col>
                <Col md={{ span: 3, offset: 10 }} style={{ display: 'flex', justifyContent: 'space-around' }}>
                    <RefreshButton  onClick={() => setAccountId(accountId)} />
                    <AddButton />
                    <EditButton />
                    <DeleteButton />
                </Col>
            </Row>
            <Row>
                <Col md={12}>
                    <Grid accountId={accountId} />
                </Col>
            </Row>
        </Container>
    );
}
