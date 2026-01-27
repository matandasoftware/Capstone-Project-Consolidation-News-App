const express = require('express');
const router = express.Router();

// GET /api/users/profile - Get user profile
router.get('/profile', (req, res) => {
  try {
    // For demo purposes, return sample user data
    res.json({ 
      id: '123',
      name: 'Demo User',
      email: 'demo@example.com',
      address: 'Sample Address',
      phone: '+27123456789'
    });
  } catch (error) {
    console.error('Error fetching user profile:', error);
    res.status(500).json({ error: 'Failed to fetch user profile' });
  }
});

// PUT /api/users/profile - Update user profile
router.put('/profile', (req, res) => {
  try {
    // For demo purposes, return success
    res.json({ message: 'Profile updated successfully', user: req.body });
  } catch (error) {
    console.error('Error updating user profile:', error);
    res.status(500).json({ error: 'Failed to update user profile' });
  }
});

module.exports = router;
