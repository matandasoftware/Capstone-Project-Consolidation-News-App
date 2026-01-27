import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage = () => {
  const vendors = [
    {
      id: 'burokos-kitchen',
      name: "Buroko's Kitchen",
      description: 'Fresh, delicious meals delivered right to your door',
      cuisine: 'Local Favorites',
      category: 'Food & Restaurants',
      rating: 4.8,
      deliveryTime: '25-40 min',
      deliveryFee: 'R14.00',
      image: '/images/logos/burokos-kitchen-logo.png',
      fallbackImage: '🍔',
      colors: ['#ff6b6b', '#4ecdc4'],
      path: '/kitchen'
    },
    {
      id: 'entertainment-hub',
      name: 'Entertainment Hub',
      description: 'Movies, games, and live events at your fingertips',
      cuisine: 'Entertainment',
      category: 'Entertainment & Events',
      rating: 0,
      deliveryTime: 'Instant Access',
      deliveryFee: 'Various',
      image: '🎬',
      fallbackImage: '🎬',
      colors: ['#ff9a9e', '#fecfef'],
      path: '#'
    },
    {
      id: 'wellness-services',
      name: 'Wellness Services',
      description: 'Health, beauty, and wellness services on demand',
      cuisine: 'Health & Beauty',
      category: 'Health & Wellness',
      rating: 0,
      deliveryTime: 'Book Now',
      deliveryFee: 'Service Fee',
      image: '💆‍♀️',
      fallbackImage: '💆‍♀️',
      colors: ['#a8edea', '#fed6e3'],
      path: '#'
    },
    {
      id: 'shopping-express',
      name: 'Shopping Express',
      description: 'Fashion, electronics, and daily essentials delivered',
      cuisine: 'Retail & Shopping',
      category: 'Shopping & Retail',
      rating: 0,
      deliveryTime: 'Same Day',
      deliveryFee: 'From R20',
      image: '🛍️',
      fallbackImage: '🛍️',
      colors: ['#ffecd2', '#fcb69f'],
      path: '#'
    },
    {
      id: 'auto-services',
      name: 'Auto Services',
      description: 'Car wash, repairs, and automotive services',
      cuisine: 'Automotive',
      category: 'Auto & Transport',
      rating: 0,
      deliveryTime: 'On-Site',
      deliveryFee: 'Service Call',
      image: '🚗',
      fallbackImage: '🚗',
      colors: ['#89f7fe', '#66a6ff'],
      path: '#'
    },
    {
      id: 'home-services',
      name: 'Home Services',
      description: 'Cleaning, repairs, and maintenance at your doorstep',
      cuisine: 'Home & Garden',
      category: 'Home & Services',
      rating: 0,
      deliveryTime: 'Scheduled',
      deliveryFee: 'Quote Based',
      image: '🏠',
      fallbackImage: '🏠',
      colors: ['#fa709a', '#fee140'],
      path: '#'
    }
  ];

  return (
    <div className="landing-page">
      <header className="landing-header">
        <div className="container">
          <div className="header-content">
            <div className="producer-brand">
              <div className="brand-logo">🏢</div>
              <h1>PRODUCER</h1>
              <p>Your Everything, Delivered</p>
            </div>
            <div className="header-stats">
              <div className="stat">
                <h3>100+</h3>
                <p>Services</p>
              </div>
              <div className="stat">
                <h3>24/7</h3>
                <p>Availability</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <section className="hero-section-landing">
        <div className="container">
          <div className="hero-content-landing">
            <h2>Discover Amazing Services</h2>
            <p>From food delivery to entertainment, wellness to shopping - everything you need in one platform</p>
            {/* Delivery info removed as requested */}
          </div>
        </div>
      </section>

      <section className="vendors-section">
        <div className="container">
          <h2 className="section-title">Popular Categories</h2>
          <div className="vendors-grid">
            {vendors.map((vendor) => (
              <div key={vendor.id} className="vendor-card">
                <div 
                  className="vendor-header"
                  style={{
                    background: `linear-gradient(135deg, ${vendor.colors[0]}, ${vendor.colors[1]})`
                  }}
                >
                  <div className="vendor-image">
                    {vendor.image && vendor.image.startsWith('/') ? (
                      <img 
                        src={vendor.image} 
                        alt={`${vendor.name} Logo`}
                        className="vendor-logo"
                        onError={(e) => {
                          e.target.style.display = 'none';
                          e.target.nextSibling.style.display = 'block';
                        }}
                      />
                    ) : null}
                    <div 
                      className="vendor-emoji" 
                      style={{ display: vendor.image && vendor.image.startsWith('/') ? 'none' : 'block' }}
                    >
                      {vendor.fallbackImage || vendor.image}
                    </div>
                  </div>
                  <div className="vendor-badge">
                    {vendor.rating > 0 ? (
                      <span>⭐ {vendor.rating}</span>
                    ) : (
                      <span>🆕 New</span>
                    )}
                  </div>
                </div>
                
                <div className="vendor-content">
                  <h3>{vendor.name}</h3>
                  <p className="vendor-description">{vendor.description}</p>
                  <div className="vendor-meta">
                    <span className="cuisine-tag">{vendor.cuisine}</span>
                    {vendor.rating > 0 ? (
                      <div className="delivery-info-card">
                        <span>🕒 {vendor.deliveryTime}</span>
                        <span>🚚 {vendor.deliveryFee}</span>
                      </div>
                    ) : (
                      <div className="coming-soon-info">
                        <span>Coming Soon</span>
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="vendor-footer">
                  {vendor.path === '#' ? (
                    <button className="vendor-btn coming-soon" disabled>
                      Coming Soon
                    </button>
                  ) : (
                    <Link to={vendor.path} className="vendor-btn">
                      Order Now
                    </Link>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <footer className="landing-footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-brand">
              <div className="brand-logo">🏢</div>
              <h3>PRODUCER</h3>
              <p>Connecting you with the best local services</p>
            </div>
            <div className="footer-links">
              <div className="link-group">
                <h4>Company</h4>
                <a href="#">About Us</a>
                <a href="#">Careers</a>
                <a href="#">Contact</a>
              </div>
              <div className="link-group">
                <h4>Support</h4>
                <a href="#">Help Center</a>
                <a href="#">Safety</a>
                <a href="#">Terms</a>
              </div>
              <div className="link-group">
                <h4>Categories</h4>
                <a href="#">Food & Restaurants</a>
                <a href="#">Entertainment</a>
                <a href="#">Wellness</a>
                <a href="#">Shopping</a>
              </div>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2025 Producer. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
