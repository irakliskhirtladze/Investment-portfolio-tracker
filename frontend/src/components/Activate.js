// src/components/Activate.js
import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

const Activate = () => {
  const { uid, token } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const activateAccount = async () => {
      try {
        await axios.post(`http://127.0.0.1:8000/auth/users/activation/`, { uid, token });
        navigate('/login');
      } catch (error) {
        console.error('Activation error:', error);
      }
    };

    activateAccount();
  }, [uid, token, navigate]);

  return <div>Activating your account...</div>;
};

export default Activate;

