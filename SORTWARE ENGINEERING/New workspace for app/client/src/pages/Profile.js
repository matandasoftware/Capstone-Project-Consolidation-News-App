import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNotification } from '../context/NotificationContext';

const Profile = () => {
  const { user, updateProfile } = useAuth();
  const { showSuccess, showError } = useNotification();
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.displayName || 'Demo User',
    email: user?.email || 'demo@example.com',
    phone: user?.phoneNumber || '+27123456789',
    address: user?.address || 'Sample Address, Thohoyandou'
  });

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  // Simple validators
  const validateEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  const validatePhone = (phone) => /^\+?\d{10,15}$/.test(phone.replace(/\s/g, ''));

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Validation
    if (!formData.name.trim()) {
      showError('Name is required.');
      return;
    }
    if (!validateEmail(formData.email)) {
      showError('Please enter a valid email address.');
      return;
    }
    if (!validatePhone(formData.phone)) {
      showError('Please enter a valid phone number (10-15 digits, can start with +).');
      return;
    }
    if (!formData.address.trim()) {
      showError('Address is required.');
      return;
    }
    setLoading(true);
    try {
      await updateProfile(formData);
      setEditing(false);
      showSuccess('Profile updated successfully!');
    } catch (error) {
      console.error('Error updating profile:', error);
      showError('Error updating profile. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page profile-page">
      <div className="container">
        <div className="profile-header">
          <h1>My Profile</h1>
          <p>Manage your account information</p>
        </div>

        <div className="profile-content">
          <div className="profile-card">
            {editing ? (
              <form onSubmit={handleSubmit} className="profile-form">
                <h2>Edit Profile</h2>
                <div className="form-group">
                  <label htmlFor="name">Full Name</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                    disabled={loading}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="email">Email Address</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                    disabled={loading}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="phone">Phone Number</label>
                  <input
                    type="tel"
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    required
                    disabled={loading}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="address">Delivery Address</label>
                  <textarea
                    id="address"
                    name="address"
                    value={formData.address}
                    onChange={handleInputChange}
                    required
                    rows="3"
                    disabled={loading}
                  />
                </div>
                <div className="form-actions">
                  <button type="button" className="btn btn-secondary" onClick={() => setEditing(false)} disabled={loading}>
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary" disabled={loading}>
                    {loading ? 'Saving...' : 'Save Changes'}
                  </button>
                </div>
                {loading && <div className="loading-spinner">Saving...</div>}
              </form>
            ) : (
              <div className="profile-info">
                <h2>Profile Information</h2>
                
                <div className="info-group">
                  <label>Full Name</label>
                  <p>{formData.name}</p>
                </div>

                <div className="info-group">
                  <label>Email Address</label>
                  <p>{formData.email}</p>
                </div>

                <div className="info-group">
                  <label>Phone Number</label>
                  <p>{formData.phone}</p>
                </div>

                <div className="info-group">
                  <label>Delivery Address</label>
                  <p>{formData.address}</p>
                </div>

                <button className="btn btn-primary" onClick={() => setEditing(true)}>
                  Edit Profile
                </button>
              </div>
            )}
          </div>

          <div className="account-actions">
            <h3>Account Actions</h3>
            <div className="action-buttons">
              <button className="btn btn-outline">Change Password</button>
              <button className="btn btn-outline">Order History</button>
              <button className="btn btn-outline">Delivery Preferences</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
