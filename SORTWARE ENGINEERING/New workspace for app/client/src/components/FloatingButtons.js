import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useCart } from '../context/CartContext';

const FloatingButtons = () => {
  const location = useLocation();
  const { getTotalItems } = useCart();

  // Don't show floating buttons on these pages
  const hiddenPaths = ['/'];

  if (hiddenPaths.includes(location.pathname)) {
    return null;
  }

  return (
    <div className="floating-buttons">
      {location.pathname !== '/' && (
        <Link to="/" className="floating-btn home-btn">
          <span>🏠</span>
        </Link>
      )}
      
      {location.pathname !== '/cart' && getTotalItems() > 0 && (
        <Link to="/cart" className="floating-btn cart-btn">
          <span>🛒</span>
          <span className="badge">{getTotalItems()}</span>
        </Link>
      )}
      
      {location.pathname !== '/profile' && (
        <Link to="/profile" className="floating-btn profile-btn">
          <span>👤</span>
        </Link>
      )}
    </div>
  );
};

export default FloatingButtons;
