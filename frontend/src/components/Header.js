import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Link } from 'react-router-dom';

const Header = () => {
  const { user, logoutUser } = useContext(AuthContext);

  return (
    <header>
      <nav>
        {user ? (
          <>
            <Link to="/">Home</Link>
            <button onClick={logoutUser}>Logout</button>
            <span>Welcome, {user.email}</span>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </nav>
    </header>
  );
};

export default Header;


