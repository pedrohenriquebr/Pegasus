import { IconButton } from '@mui/material';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';

import MenuIcon from '@mui/icons-material/Menu';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import CategoryIcon from '@mui/icons-material/Category';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import CloudDownloadIcon from '@mui/icons-material/CloudDownload';
import SettingsIcon from '@mui/icons-material/Settings';

export default function MainMenu (){
    const [anchorEl, setAnchorEl] = useState(null);
    const open = Boolean(anchorEl);
    const { t } = useTranslation();
    
    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
        setAnchorEl(null);
    };

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
                <MenuIcon />
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
                <MenuItem onClick={handleClose}><AccountBalanceIcon style={{ color: '#FFC13D', marginRight: 10 }} /> {t('appbar.appmenu.accounts')}</MenuItem>
                <MenuItem onClick={handleClose}><CategoryIcon style={{ color: '#F86A2B', marginRight: 10 }} /> {t('appbar.appmenu.categories')}</MenuItem>
                <MenuItem onClick={handleClose}><CloudUploadIcon style={{ color: '#38AFF4', marginRight: 10 }} /> {t('appbar.appmenu.import')}</MenuItem>
                <MenuItem onClick={handleClose}><CloudDownloadIcon style={{ color: 'primary', marginRight: 10 }} />{t('appbar.appmenu.export')}</MenuItem>
                <MenuItem onClick={handleClose}><SettingsIcon style={{ color: 'secondary', marginRight: 10 }} />{t('appbar.appmenu.settings')}</MenuItem>
            </Menu>
        </div>
    )
}
