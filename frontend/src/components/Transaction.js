import React, { useContext, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';

const Transaction = () => {
  const { user, logoutUser } = useContext(AuthContext);
  const [transaction, setTransaction] = useState({
    transaction_date: '',
    asset_type: 'stock',
    symbol: '',
    transaction_type: 'buy',
    quantity: '',
    trade_price: '',
    commission: '',
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setTransaction({ ...transaction, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/transactions/create-investment-transaction/', transaction);
      alert('Transaction successfully created.');
      navigate('/');
    } catch (error) {
      console.error('Error creating transaction:', error);
    }
  };

  return (
    <div>
      <header>
        <button onClick={logoutUser}>Logout</button>
        <span>Welcome, {user.email}</span>
      </header>
      <main>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Transaction Date:</label>
            <input
              type="date"
              name="transaction_date"
              value={transaction.transaction_date}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label>Asset Type:</label>
            <select name="asset_type" value={transaction.asset_type} onChange={handleChange}>
              <option value="stock">Stock</option>
              <option value="crypto">Crypto</option>
            </select>
          </div>
          <div>
            <label>Symbol:</label>
            <input
              type="text"
              name="symbol"
              value={transaction.symbol}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label>Transaction Type:</label>
            <select name="transaction_type" value={transaction.transaction_type} onChange={handleChange}>
              <option value="buy">Buy</option>
              <option value="sell">Sell</option>
            </select>
          </div>
          <div>
            <label>Quantity:</label>
            <input
              type="number"
              name="quantity"
              value={transaction.quantity}
              onChange={handleChange}
              required
            />
          </div>
          <div>
            <label>Trade Price:</label>
            <input
              type="number"
              name="trade_price"
              value={transaction.trade_price}
              onChange={handleChange}
            />
          </div>
          <div>
            <label>Commission:</label>
            <input
              type="number"
              name="commission"
              value={transaction.commission}
              onChange={handleChange}
              required
            />
          </div>
          <button type="submit">Submit</button>
        </form>
      </main>
    </div>
  );
};

export default Transaction;
