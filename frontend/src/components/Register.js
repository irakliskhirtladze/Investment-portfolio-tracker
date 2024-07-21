import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rePassword, setRePassword] = useState('');
  const { registerUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await registerUser(email, password, rePassword);
      navigate('/login');
    } catch (error) {
      console.error('Error during registration:', error.response ? error.response.data : error.message);
      alert('Registration failed. Please try again.');
    }
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        </div>
        <div>
          <label>Password:</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        <div>
          <label>Confirm Password:</label>
          <input type="password" value={rePassword} onChange={(e) => setRePassword(e.target.value)} />
        </div>
        <button type="submit">Register</button>
      </form>
      <p>
        Log in if you already have an account. <Link to="/login">Login</Link>
      </p>
    </div>
  );
};

export default Register;
