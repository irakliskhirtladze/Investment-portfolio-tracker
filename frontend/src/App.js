import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Header from './components/Header';
import Footer from './components/Footer';
import Login from './components/Login';
import Register from './components/Register';
import Activate from './components/Activate';
import Home from './components/Home';
import Transaction from './components/Transaction';
import InitialSetup from './components/InitialSetup';

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Header />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/activate/:uid/:token" element={<Activate />} />
          <Route path="/transaction" element={<Transaction />} />
          <Route path="/initial-setup" element={<InitialSetup />} />
          <Route path="/" element={<Home />} />
        </Routes>
        <Footer />
      </Router>
    </AuthProvider>
  );
};

export default App;

