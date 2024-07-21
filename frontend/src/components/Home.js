import React, { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import api from '../services/api';
import { Link } from 'react-router-dom';

const Home = () => {
  const { user, logoutUser } = useContext(AuthContext);
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPortfolio = async () => {
      try {
        const response = await api.get('/portfolio/');
        setPortfolio(response.data);
        setLoading(false);
      } catch (error) {
        console.error(error);
      }
    };

    fetchPortfolio();
  }, []);

  const handleRefresh = async () => {
    try {
      await api.post('/portfolio/refresh/');
      const response = await api.get('/portfolio/');
      setPortfolio(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <header>
        <nav>
          <button onClick={logoutUser}>Logout</button>
          <span>Welcome, {user.email}</span>
        </nav>
      </header>
      <main>
        {portfolio.cash_balance ? (
          <>
            <Link to="/transaction">Make a transaction</Link>
            <Link to="/initial-setup">Reset portfolio</Link>
            <button onClick={handleRefresh}>Refresh portfolio</button>
            <div>Total portfolio value: {portfolio.total_value}</div>
            <div>Cash balance: {portfolio.cash_balance}</div>
            {portfolio.assets.length > 0 ? (
              <table>
                <thead>
                  <tr>
                    <th>Asset</th>
                    <th>Quantity</th>
                    <th>Current Value</th>
                  </tr>
                </thead>
                <tbody>
                  {portfolio.assets.map((asset) => (
                    <tr key={asset.id}>
                      <td>{asset.asset_symbol}</td>
                      <td>{asset.quantity}</td>
                      <td>{asset.current_value}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div>No assets in portfolio.</div>
            )}
          </>
        ) : (
          <>
            <Link to="/transaction">Make a transaction</Link>
            <Link to="/initial-setup">Initial setup</Link>
          </>
        )}
      </main>
    </div>
  );
};

export default Home;


