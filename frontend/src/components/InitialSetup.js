import React, { useContext, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';

const InitialSetup = () => {
  const { user, logoutUser } = useContext(AuthContext);
  const [cashBalance, setCashBalance] = useState('');
  const [assets, setAssets] = useState([{ asset_type: '', asset_symbol: '', quantity: '' }]);
  const navigate = useNavigate();

  const handleAddAsset = () => {
    setAssets([...assets, { asset_type: '', asset_symbol: '', quantity: '' }]);
  };

  const handleRemoveAsset = (index) => {
    const newAssets = assets.filter((_, i) => i !== index);
    setAssets(newAssets);
  };

  const handleChangeAsset = (index, field, value) => {
    const newAssets = assets.map((asset, i) => (i === index ? { ...asset, [field]: value } : asset));
    setAssets(newAssets);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/initial-setup/', { cash_balance: cashBalance, assets });
      alert('Initial setup completed successfully.');
      navigate('/');
    } catch (error) {
      console.error('Error during initial setup:', error);
    }
  };

  return (
    <div>
      <header>
        <button onClick={logoutUser}>Logout</button>
        <span>Welcome, {user.email}</span>
      </header>
      <main>
        <p>Warning: This action will delete all existing data including transaction history.</p>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Cash Balance:</label>
            <input
              type="number"
              value={cashBalance}
              onChange={(e) => setCashBalance(e.target.value)}
              required
            />
          </div>
          {assets.map((asset, index) => (
            <div key={index}>
              <label>Asset Type:</label>
              <input
                type="text"
                value={asset.asset_type}
                onChange={(e) => handleChangeAsset(index, 'asset_type', e.target.value)}
                required
              />
              <label>Asset Symbol:</label>
              <input
                type="text"
                value={asset.asset_symbol}
                onChange={(e) => handleChangeAsset(index, 'asset_symbol', e.target.value)}
                required
              />
              <label>Quantity:</label>
              <input
                type="number"
                value={asset.quantity}
                onChange={(e) => handleChangeAsset(index, 'quantity', e.target.value)}
                required
              />
              <button type="button" onClick={() => handleRemoveAsset(index)}>
                Remove
              </button>
            </div>
          ))}
          <button type="button" onClick={handleAddAsset}>
            Add Asset
          </button>
          <button type="submit">Submit</button>
        </form>
      </main>
    </div>
  );
};

export default InitialSetup;
