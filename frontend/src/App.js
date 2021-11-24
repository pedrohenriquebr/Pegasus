
import TransactionPage  from './app/pages/Transactions';
import ImportationPage  from './app/pages/ImportationPage';
import { HomeAppBar } from './app/pages/components/HomeAppBar';

import Container from 'react-bootstrap/Container';

import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";

function App() {
  return (
      <div>
        <HomeAppBar></HomeAppBar>
        <Container expand="lg">
        <Router>
          <Routes>
            <Route path="/transactions" element={<TransactionPage />} />
            <Route path="/transactions/importation" element={<ImportationPage />} />
            <Route path="/" element={<TransactionPage />} />
          </Routes>
        </Router>
        </Container>
      </div>
  );
}

export default App;
