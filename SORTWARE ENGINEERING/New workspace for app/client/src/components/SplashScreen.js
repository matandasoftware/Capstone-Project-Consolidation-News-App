import React, { useEffect, useState } from 'react';

const SplashScreen = ({ onComplete }) => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false);
      setTimeout(() => {
        onComplete();
      }, 500); // Wait for fade out animation
    }, 3000); // Show splash for 3 seconds

    return () => clearTimeout(timer);
  }, [onComplete]);

  if (!isVisible) {
    return (
      <div className={`splash-screen fade-out`}>
        <div className="splash-content">
          <div className="producer-logo">
            <div className="logo-placeholder">
              <img 
                src="/images/logos/producer-logo.png" 
                alt="Producer Logo" 
                className="producer-logo-img"
                onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.nextSibling.style.display = 'block';
                }}
              />
              <div className="fallback-logo" style={{ display: 'none' }}>
                <h1>PRODUCER</h1>
                <div className="logo-icon">🏢</div>
                <p>Food Delivery Platform</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="splash-screen">
      <div className="splash-content">
        <div className="producer-logo">
          <div className="logo-placeholder">
            <img 
              src="/images/logos/producer-logo.png" 
              alt="Producer Logo" 
              className="producer-logo-img"
              onError={(e) => {
                e.target.style.display = 'none';
                e.target.nextSibling.style.display = 'block';
              }}
            />
            <div className="fallback-logo" style={{ display: 'none' }}>
              <h1>PRODUCER</h1>
              <div className="logo-icon">🏢</div>
              <p>Food Delivery Platform</p>
            </div>
          </div>
          <div className="loading-animation">
            <div className="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SplashScreen;
