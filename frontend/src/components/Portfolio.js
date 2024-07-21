import React, { useState, useEffect } from 'react';
import axios from '../services/api';

const Portfolio = () => {
  const [portfolio, setPortfolio] = useState([]);

  useEffect(() => {
    const fetchPortfolio = async () => {
      try {
        const response = await axios.get('/portfolio/');
        setPortfolio(response.data.results);
      } catch (error) {
        console.error('Error fetching portfolio:', error);
      }
    };

    fetchPortfolio();
  }, []);

  return (
    <div>
      <h1>Portfolio</h1>
      <ul>
        {portfolio.map(entry => (
          <li key={entry.id}>{entry.asset_symbol}: {entry.current_value}</li>
        ))}
      </ul>
    </div>
  );
};

export default Portfolio;
