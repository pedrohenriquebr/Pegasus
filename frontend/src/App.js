
import TransactionPage  from './app/pages/Transactions';
import { HomeAppBar } from './app/pages/components/HomeAppBar';

import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";

function App() {
  return (
      <div>
        <HomeAppBar></HomeAppBar>
        <Router>
          <Routes>
            <Route path="/transactions" element={<TransactionPage />} />
            <Route path="/" element={<TransactionPage />} />
          </Routes>
        </Router>
      </div>
  );
}

export default App;
