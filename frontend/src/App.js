
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { themeOptions } from './theme';
import TransactionPage  from './app/pages/Transactions';
import { HomeAppBar } from './app/pages/components/HomeAppBar';

import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";

const theme  = createTheme(themeOptions);
function App() {
  return (
    <ThemeProvider theme={theme}>
      <HomeAppBar></HomeAppBar>
      <Router>
        <Routes>
          <Route path="/transactions" element={<TransactionPage />} />
          <Route path="/" element={<TransactionPage />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
