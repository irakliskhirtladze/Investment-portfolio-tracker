import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { activateUser } from '../services/api';

const Activate = () => {
  const { uid, token } = useParams();

  useEffect(() => {
    const activate = async () => {
      try {
        await activateUser(uid, token);
        alert('Your account has been activated. You can now log in.');
      } catch (error) {
        alert('Activation failed. Please try again or contact support.');
      }
    };

    activate();
  }, [uid, token]);

  return <div>Activating...</div>;
};

export default Activate;

