import { useTranslation } from 'react-i18next';
import {BsTranslate} from 'react-icons/bs'; 
import Dropdown from 'react-bootstrap/Dropdown';

const lngs = {
    en: { nativeName: 'English' },
    ptBr: { nativeName: 'Português' }
};


export default function TranslateMenu() {
    const { t, i18n } = useTranslation();

    const changeLanguage = (lng) => {
        i18n.changeLanguage(lng)
    }
    
    return (
        <Dropdown>
            <Dropdown.Toggle color="blue" id="dropdown-basic">
                <BsTranslate />
            </Dropdown.Toggle>
            <Dropdown.Menu>
            {Object.keys(lngs).map((lng) => (
            <Dropdown.Item key={lng} onClick={(ev) => changeLanguage(lng)}>
                    {lngs[lng].nativeName}
            </Dropdown.Item>))}
            </Dropdown.Menu>
        </Dropdown>
    );
}
