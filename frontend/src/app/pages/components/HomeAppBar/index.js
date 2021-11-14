
import AppBar from '@mui/material/AppBar';
import { Toolbar } from '@mui/material';
import Typography from '@mui/material/Typography';

import MainMenu from '../MainMenu';
import TranslateMenu from '../TranslateMenu';


export const HomeAppBar = () => {
    return (
        <AppBar position="static">
            <Toolbar>
                <MainMenu />
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    Pegasus
                </Typography>
                <TranslateMenu />
            </Toolbar>
        </AppBar>
    )
}