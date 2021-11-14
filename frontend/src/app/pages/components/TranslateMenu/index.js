import { useState,} from 'react';
import { useTranslation } from 'react-i18next';
import IconButton from '@mui/material/IconButton';
import MenuItem from '@mui/material/MenuItem';
import Menu from '@mui/material/Menu';
import TranslateIcon from '@mui/icons-material/Translate';
import Typography from '@mui/material/Typography';

const lngs = {
    en: { nativeName: 'English' },
    ptBr: { nativeName: 'Português' }
};


export default function TranslateMenu() {
    const [anchorEl, setAnchorEl] = useState(null);
    const open = Boolean(anchorEl);
    const { t, i18n } = useTranslation();

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

    const changeLanguage = (lng) => {
        i18n.changeLanguage(lng)
        handleClose();
    }
    
    return (
        <div>
            <IconButton
                size="large"
                edge="start"
                color="inherit"
                aria-controls="basic-menu"
                aria-haspopup="true"
                aria-expanded={open ? 'true' : undefined}
                onClick={handleClick}
            >
                <TranslateIcon />
                </IconButton>
                    <Menu
                        id="basic-menu"
                        anchorEl={anchorEl}
                        open={open}
                        onClose={handleClose}
                        MenuListProps={{
                            'aria-labelledby': 'basic-button',
                        }}
                    >

                        {Object.keys(lngs).map((lng) => (
                            <MenuItem key={lng} onClick={(ev) => changeLanguage(lng)}>
                                <Typography variant="body1">
                                    {lngs[lng].nativeName}
                                </Typography>
                            </MenuItem>
                        ))}

                    </Menu>
        </div>
    );
}
