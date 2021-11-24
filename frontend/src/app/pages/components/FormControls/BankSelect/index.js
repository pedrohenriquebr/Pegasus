import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import api from '../../../../services/api';

import Form from 'react-bootstrap/Form';
export default function BankSelect({ onBankChange, isInvalid, children, ...props }) {
    const [bank, setBank] = useState('1');
    const { t } = useTranslation();

    const handleChange = (event) => {
        setBank(event.target.value);
        if (onBankChange) onBankChange(event.target.value);
    };

    return (
        <Form.Group {...props}>
            <Form.Label>Select a bank</Form.Label>
            <Form.Select isInvalid={isInvalid} aria-label="Default select example" onChange={handleChange} defaultValue={bank}>
                <option value="0">{t('labels.bank')}</option>
                <option value="inter">Inter</option>
            </Form.Select>
            {children}
        </Form.Group>
    )
}