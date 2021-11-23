import { useTranslation } from 'react-i18next';
import Dropdown from 'react-bootstrap/Dropdown';
import { AiOutlineMenu } from "react-icons/ai";
export default function MainMenu() {

    const { t } = useTranslation();

    return (
        <Dropdown>
            <Dropdown.Toggle variant="success" id="dropdown-basic">
                <AiOutlineMenu />
            </Dropdown.Toggle>
            <Dropdown.Menu>
                <Dropdown.Item href="#">{t('appbar.appmenu.accounts')}</Dropdown.Item>
                <Dropdown.Item href="#">{t('appbar.appmenu.categories')}</Dropdown.Item>
                <Dropdown.Item href="#">{t('appbar.appmenu.import')}</Dropdown.Item>
                <Dropdown.Item href="#">{t('appbar.appmenu.export')}</Dropdown.Item>
                <Dropdown.Item href="#">{t('appbar.appmenu.settings')}</Dropdown.Item>
            </Dropdown.Menu>
        </Dropdown>
    )
}
