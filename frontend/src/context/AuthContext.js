import React, { createContext, useState, useEffect } from 'react';
import { login, register } from '../services/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const loginUser = async (email, password) => {
    try {
      const response = await login(email, password);
      if (response.data) {
        setUser(response.data.user);
        localStorage.setItem('user', JSON.stringify(response.data.user));
        localStorage.setItem('token', response.data.access);
      }
    } catch (error) {
      console.error('Error during login:', error);
      throw error;
    }
  };

  const registerUser = async (email, password, re_password) => {
    try {
      const response = await register(email, password, re_password);
      if (response.data) {
        setUser(response.data.user);
      }
    } catch (error) {
      console.error('Error during registration:', error.response ? error.response.data : error.message);
      throw error;
    }
  };

  const logoutUser = () => {
    setUser(null);
    localStorage.removeItem('user');
    localStorage.removeItem('token');
  };

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, loginUser, registerUser, logoutUser }}>
      {children}
    </AuthContext.Provider>
  );
};
