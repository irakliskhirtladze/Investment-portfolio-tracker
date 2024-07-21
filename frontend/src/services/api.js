import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const login = (email, password) => {
  return api.post('/auth/jwt/create/', { email, password });
};

export const register = (email, password, re_password) => {
  return api.post('/auth/users/', { email, password, re_password });
};

export const activateUser = (uid, token) => {
  return api.post('/auth/users/activation/', { uid, token });
};

export const getPortfolio = () => {
  return api.get('/api/portfolio/');
};

export const initialSetup = (cash_balance, assets) => {
  return api.post('/api/initial-setup/', { cash_balance, assets });
};

export const createInvestmentTransaction = (transaction) => {
  return api.post('/api/transactions/create-investment-transaction/', transaction);
};

export const refreshPortfolio = () => {
  return api.post('/api/portfolio/refresh/');
};

export default api;
