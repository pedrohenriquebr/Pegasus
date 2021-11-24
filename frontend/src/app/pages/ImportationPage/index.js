import { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Toast from 'react-bootstrap/Toast';
import ToastContainer from 'react-bootstrap/ToastContainer';

import AccountSelect from '../components/formcontrols/AccountSelect';
import BankSelect from '../components/formcontrols/BankSelect';

import api from '../../services/api';
import { useTranslation } from 'react-i18next';


const Toastr = ({variant, message, title, time, show, ...props}) => {
    return (
        <ToastContainer className="p-3" position='top-end'>
            <Toast show={show} {...props} className="d-inline-block m-1" bg={variant} autohide>
                <Toast.Header>
                    <strong className="me-auto">{title}</strong>
                    <small>{Math.round(time / 1000)} secs ago</small>
                </Toast.Header>
                <Toast.Body>
                    {message}
                </Toast.Body>
            </Toast>
        </ToastContainer>
    )
}


export default function ImportationPage() {
    const [form, setForm] = useState({});
    const [errors, setErrors] = useState({});
    const [toastr, setToastr] = useState({
        show: false,
        variant: 'success',
        title: '',
        message: ''
    });

    const { t } = useTranslation();


    const sendForm = () => {
        let formData = new FormData();
        formData.append('id_account', form.accountId);
        formData.append('bank', form.bankName.toLowerCase());
        formData.append('file', form.file);
        let now  = new Date(Date.now());

        api.post('/export/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then(d => {
            setToastr({
                show: true,
                time: new Date(Date.now()) - now,
                variant: d.data.status == 'error' ? 'danger': d.data.status,
                title: d.data.status == 'error' ? t('error') : t('success'),
                message: d.data.message || d.data.error
            });
        })

    }


    const setField = (field, value) => {
        setForm({
            ...form,
            [field]: value
        })
        // Check and see if errors exist, and remove them from the error object:
        if (!!errors[field]) setErrors({
            ...errors,
            [field]: null
        })
    }

    const findFormErrors = () => {
        const { bankName, accountId, file } = form
        const newErrors = {}
        // bank name errors
        if (!bankName || bankName === '') newErrors.bankName = 'cannot be blank!'
        else if (bankName.length > 30) newErrors.bankName = 'name is too long!'

        // account errors
        if (!accountId || accountId === '' || accountId == 0) newErrors.accountId = 'cannot be blank!'

        // account errors
        if (!file || file == undefined) newErrors.file = 'cannot be blank!'
        return newErrors
    }

    const handleSubmit = e => {
        e.preventDefault()

        // get our new errors
        const newErrors = findFormErrors()
        // Conditional logic:
        if (Object.keys(newErrors).length > 0) {
            // We got errors!
            setErrors(newErrors)
        } else {
            // No errors! Put any logic here for the form submission!
            sendForm()
        }
    }


    return (
        <Row className="justify-content-md-center">
            <Form onSubmit={handleSubmit}>
                <AccountSelect
                    as={Col}
                    md={3}
                    controlId="accountId"
                    isInvalid={!!errors.accountId}
                    onAccountChange={(d) => setField('accountId', d)} >
                    <Form.Control.Feedback type='invalid'>
                        {errors.accountId}
                    </Form.Control.Feedback>
                </AccountSelect>

                <BankSelect
                    as={Col}
                    md={3}
                    controlId="bankName"
                    isInvalid={!!errors.bankName}
                    onBankChange={(d) => setField('bankName', d)} >
                    <Form.Control.Feedback type='invalid'>
                        {errors.bankName}
                    </Form.Control.Feedback>
                </BankSelect>



                <Row>
                    <Form.Group
                        as={Col}
                        md={3} controlId="formFile">
                        <Form.Label>Select your file</Form.Label>
                        <Form.Control type="file"
                            isInvalid={!!errors.file}
                            onChange={(e) => setField('file', e.target.files[0])} />
                        <Form.Control.Feedback type='invalid'>
                            {errors.file}
                        </Form.Control.Feedback>
                    </Form.Group>
                </Row>
                <Row>
                    <Col >
                        <Button variant="primary" type="submit">
                            Submit
                        </Button>
                    </Col>
                </Row>
            </Form>

            <Toastr variant={toastr.variant}
                time={toastr.time}
                title={toastr.title}
                message={toastr.message}
                show={toastr.show}
                onClose={() => setToastr(e => ({ ...e, show: false }))} />
        </Row>
    )
}