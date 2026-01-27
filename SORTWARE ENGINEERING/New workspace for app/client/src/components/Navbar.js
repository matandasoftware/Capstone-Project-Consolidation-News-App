import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const { getTotalItems } = useCart();
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const isActive = (path) => location.pathname === path;

  const handleLogout = async () => {
    try {
      await logout();
      setIsMenuOpen(false);
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <Link to="/" className="navbar-brand" onClick={closeMenu}>
          Buroko's Kitchen
        </Link>

        <button className="mobile-menu-toggle" onClick={toggleMenu}>
          <span className={`hamburger ${isMenuOpen ? 'active' : ''}`}>
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>

        <ul className={`navbar-nav ${isMenuOpen ? 'mobile-open' : ''}`}>
          <li>
            <Link 
              to="/" 
              className={`nav-link ${isActive('/') ? 'active' : ''}`}
              onClick={closeMenu}
            >
              <span>🏠</span>
              Home
            </Link>
          </li>
          <li>
                <Link 
                  to="/kitchen/menu" 
                  className={`nav-link ${isActive('/kitchen/menu') ? 'active' : ''}`}
                  onClick={closeMenu}
                >
                  <span>📋</span>
                  Menu
                </Link>
          </li>
          <li>
                <Link 
                  to="/kitchen/cart" 
                  className={`nav-link ${isActive('/kitchen/cart') ? 'active' : ''}`}
                  onClick={closeMenu}
                  style={{ position: 'relative' }}
                >
                  <span>🛒</span>
                  Cart
                  {getTotalItems() > 0 && (
                    <span className="cart-badge">
                      {getTotalItems()}
                    </span>
                  )}
                </Link>
          </li>
          
          {user ? (
            <>
              <li>
                <Link 
                  to="/profile" 
                  className={`nav-link ${isActive('/profile') ? 'active' : ''}`}
                  onClick={closeMenu}
                >
                  <span>👤</span>
                  Profile
                </Link>
              </li>
              <li>
                <button 
                  onClick={handleLogout}
                  className="nav-link logout-btn"
                >
                  <span>🚪</span>
                  Logout
                </button>
              </li>
            </>
          ) : (
            <li>
              <Link 
                to="/kitchen/login" 
                className={`nav-link ${isActive('/kitchen/login') ? 'active' : ''}`}
                onClick={closeMenu}
              >
                <span>👤</span>
                Login
              </Link>
            </li>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
