import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="home-page">
      {/* ...existing code... */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-text">
            <h1 className="hero-title">
              Welcome to <span className="brand-name">Buroko's Kitchen</span>
            </h1>
            <p className="hero-subtitle">
              Fresh, delicious meals delivered right to your door in Thohoyandou
            </p>
            <Link to="/menu" className="cta-button">
              Order Now
            </Link>
          </div>
          <div className="hero-image">
            <img 
              src="/images/hero-food.jpg" 
              alt="Delicious food from Buroko's Kitchen" 
              className="hero-img"
            />
          </div>
        </div>
      </section>

      <section className="info-section">
        <div className="info-grid">
          <div className="info-card">
            <div className="info-icon">📍</div>
            <h3>Delivery Area</h3>
            <p>Thohoyandou</p>
          </div>
          
          <div className="info-card">
            <div className="info-icon">🚚</div>
            <h3>Delivery Fee</h3>
            <p>R14.00</p>
          </div>
          
          <div className="info-card">
            <div className="info-icon">🕒</div>
            <h3>Opening Hours</h3>
            <p>Mon–Fri: 09:00–18:00</p>
            <p>Sat: 09:00–16:00</p>
          </div>
          
          <div className="info-card">
            <div className="info-icon">⭐</div>
            <h3>Quality Promise</h3>
            <p>Fresh ingredients, made with love</p>
          </div>
        </div>
      </section>

      <section className="features-section">
        <div className="container">
          <h2>Why Choose Buroko's Kitchen?</h2>
          <div className="features-grid">
            <div className="feature-card">
              <h3>🥗 Fresh Ingredients</h3>
              <p>We source the freshest ingredients daily to ensure the best quality meals.</p>
            </div>
            
            <div className="feature-card">
              <h3>⚡ Fast Delivery</h3>
              <p>Quick and reliable delivery service throughout Thohoyandou area.</p>
            </div>
            
            <div className="feature-card">
              <h3>💰 Great Value</h3>
              <p>Affordable prices without compromising on quality or taste.</p>
            </div>
            
            <div className="feature-card">
              <h3>📱 Easy Ordering</h3>
              <p>Simple online ordering system for a seamless experience.</p>
            </div>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="container">
          <h2>Ready to Order?</h2>
          <p>Browse our delicious menu and place your order today!</p>
          <Link to="/menu" className="cta-button secondary">
            View Menu
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;
