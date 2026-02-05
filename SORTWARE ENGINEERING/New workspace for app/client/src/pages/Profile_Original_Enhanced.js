import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useNotification } from '../context/NotificationContext';

const ProfileOriginalEnhanced = () => {
  const navigate = useNavigate();
  const { showSuccess, showError } = useNotification();
  const [profile, setProfile] = useState({
    name: '',
    phone: '',
    address: '',
    time: '',
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem('customerProfile');
    if (stored) {
      try {
        setProfile(JSON.parse(stored));
      } catch (err) {
        console.error('Error loading profile:', err);
      }
    }
  }, []);

  const validateForm = () => {
    const newErrors = {};

    if (!profile.name.trim()) {
      newErrors.name = 'Name is required';
    } else if (profile.name.length < 2) {
      newErrors.name = 'Name must be at least 2 characters';
    }

    if (!profile.phone.trim()) {
      newErrors.phone = 'Phone number is required';
    } else if (!/^(\+27|0)[0-9]{9}$/.test(profile.phone.replace(/\s/g, ''))) {
      newErrors.phone = 'Please enter a valid South African phone number';
    }

    if (!profile.address.trim()) {
      newErrors.address = 'Delivery address is required';
    } else if (profile.address.length < 10) {
      newErrors.address = 'Please provide a complete address';
    }

    if (profile.time && !/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]/.test(profile.time)) {
      newErrors.time = 'Time format should be HH:MM (e.g., 14:30)';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfile(prev => ({
      ...prev,
      [name]: value,
    }));

    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: '',
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      showError('Please fix the errors below');
      return;
    }

    setIsLoading(true);

    try {
      // Format phone number
      const formattedProfile = {
        ...profile,
        phone: profile.phone.replace(/\s/g, ''),
        address: profile.address.trim(),
        name: profile.name.trim(),
      };

      localStorage.setItem('customerProfile', JSON.stringify(formattedProfile));
      
      setTimeout(() => {
        showSuccess('Profile saved successfully! 🎉');
        setIsLoading(false);
        navigate('/kitchen/cart');
      }, 1000);
    } catch (err) {
      console.error('Error saving profile:', err);
      showError('Failed to save profile');
      setIsLoading(false);
    }
  };

  const formatPhoneNumber = (value) => {
    // Remove all non-digits
    const digits = value.replace(/\D/g, '');
    
    // Format as South African number
    if (digits.length >= 10) {
      if (digits.startsWith('27')) {
        return `+${digits.slice(0, 2)} ${digits.slice(2, 4)} ${digits.slice(4, 7)} ${digits.slice(7, 11)}`;
      } else if (digits.startsWith('0')) {
        return `${digits.slice(0, 3)} ${digits.slice(3, 6)} ${digits.slice(6, 10)}`;
      }
    }
    return value;
  };

  const handlePhoneChange = (e) => {
    const formatted = formatPhoneNumber(e.target.value);
    setProfile(prev => ({
      ...prev,
      phone: formatted,
    }));

    if (errors.phone) {
      setErrors(prev => ({
        ...prev,
        phone: '',
      }));
    }
  };

  return (
    <div className="page profile-page-enhanced">
      <div className="container">
        <div className="profile-header">
          <h1>👤 Your Profile</h1>
          <p>Complete your details for delivery</p>
        </div>

        <div className="profile-content">
          <div className="profile-info-card">
            <div className="delivery-area-info">
              <h3>📍 Delivery Information</h3>
              <div className="delivery-details">
                <div className="delivery-item">
                  <span className="icon">🏠</span>
                  <div>
                    <strong>Delivery Area:</strong>
                    <p>Thohoyandou and surrounding areas</p>
                  </div>
                </div>
                <div className="delivery-item">
                  <span className="icon">💰</span>
                  <div>
                    <strong>Delivery Fee:</strong>
                    <p>R14.00</p>
                  </div>
                </div>
                <div className="delivery-item">
                  <span className="icon">⏰</span>
                  <div>
                    <strong>Operating Hours:</strong>
                    <p>Mon-Fri: 09:00-18:00<br />Sat: 09:00-16:00</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="profile-form-card">
            <form onSubmit={handleSubmit} className="profile-form">
              <h3>✏️ Customer Details</h3>
              
              <div className="form-group">
                <label htmlFor="name">
                  <span className="field-icon">👤</span>
                  Full Name *
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={profile.name}
                  onChange={handleChange}
                  placeholder="Enter your full name"
                  className={errors.name ? 'error' : ''}
                  disabled={isLoading}
                  required
                />
                {errors.name && <span className="error-message">{errors.name}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="phone">
                  <span className="field-icon">📞</span>
                  Phone Number *
                </label>
                <input
                  type="tel"
                  id="phone"
                  name="phone"
                  value={profile.phone}
                  onChange={handlePhoneChange}
                  placeholder="081 234 5678 or +27 81 234 5678"
                  className={errors.phone ? 'error' : ''}
                  disabled={isLoading}
                  required
                />
                {errors.phone && <span className="error-message">{errors.phone}</span>}
                <small className="field-help">
                  We'll contact you via WhatsApp for order updates
                </small>
              </div>

              <div className="form-group">
                <label htmlFor="address">
                  <span className="field-icon">🏠</span>
                  Delivery Address *
                </label>
                <textarea
                  id="address"
                  name="address"
                  value={profile.address}
                  onChange={handleChange}
                  placeholder="Enter your complete delivery address (street, suburb, landmarks)"
                  className={errors.address ? 'error' : ''}
                  disabled={isLoading}
                  rows="3"
                  required
                />
                {errors.address && <span className="error-message">{errors.address}</span>}
                <small className="field-help">
                  Include landmarks or building details for easier delivery
                </small>
              </div>

              <div className="form-group">
                <label htmlFor="time">
                  <span className="field-icon">⏰</span>
                  Preferred Delivery Time (Optional)
                </label>
                <input
                  type="text"
                  id="time"
                  name="time"
                  value={profile.time}
                  onChange={handleChange}
                  placeholder="e.g., 14:00 or 2:00 PM"
                  className={errors.time ? 'error' : ''}
                  disabled={isLoading}
                />
                {errors.time && <span className="error-message">{errors.time}</span>}
                <small className="field-help">
                  You can also select from suggested times during checkout
                </small>
              </div>

              <div className="form-actions">
                <button 
                  type="button" 
                  onClick={() => navigate('/kitchen/')}
                  className="btn-secondary"
                  disabled={isLoading}
                >
                  Cancel
                </button>
                
                <button 
                  type="submit" 
                  className="btn-primary"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <span>
                      <span className="loading-spinner"></span>
                      Saving...
                    </span>
                  ) : (
                    <span>
                      💾 Save Profile
                    </span>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>

        <div className="tips-section">
          <h3>💡 Tips</h3>
          <div className="tips-grid">
            <div className="tip-item">
              <span className="tip-icon">📱</span>
              <div>
                <strong>WhatsApp Orders</strong>
                <p>All orders are confirmed via WhatsApp for fastest service</p>
              </div>
            </div>
            <div className="tip-item">
              <span className="tip-icon">💳</span>
              <div>
                <strong>Payment Method</strong>
                <p>Secure EFT payment via Capitec Bank</p>
              </div>
            </div>
            <div className="tip-item">
              <span className="tip-icon">🚚</span>
              <div>
                <strong>Delivery Time</strong>
                <p>Orders typically delivered within 60-90 minutes</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileOriginalEnhanced;
