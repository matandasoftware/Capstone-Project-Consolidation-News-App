const express = require('express');
const router = express.Router();
const MenuItem = require('../models/MenuItem');

// Sample menu data
const sampleMenuItems = [
  {
    name: 'Ayoba Special',
    description: 'Wrap + egg + patty with special sauce',
    price: 65,
    category: 'wraps',
    popular: true,
    available: true
  },
  {
    name: 'Siphos Combo',
    description: 'Chips, polony, lettuce & half loaf bread',
    price: 45,
    category: 'combos',
    popular: false,
    available: true
  },
  {
    name: 'Classic Burger',
    description: 'Beef patty, lettuce, tomato, cheese, special sauce',
    price: 55,
    category: 'burgers',
    popular: true,
    available: true
  },
  {
    name: 'Chicken Wrap',
    description: 'Grilled chicken, vegetables, sauce in soft wrap',
    price: 50,
    category: 'wraps',
    popular: false,
    available: true
  },
  {
    name: 'Russian & Chips',
    description: '3 Russians with brown bread, atchar, polony',
    price: 40,
    category: 'combos',
    popular: false,
    available: true
  },
  {
    name: 'Veggie Delight',
    description: 'Fresh vegetables, hummus, avocado wrap',
    price: 45,
    category: 'wraps',
    popular: false,
    available: true
  }
];

// GET /api/menu - Get all menu items
router.get('/', async (req, res) => {
  try {
    // Return sample data for now (in production, this would come from database)
    res.json(sampleMenuItems);
  } catch (error) {
    console.error('Error fetching menu:', error);
    res.status(500).json({ error: 'Failed to fetch menu items' });
  }
});

// GET /api/menu/:id - Get specific menu item
router.get('/:id', async (req, res) => {
  try {
    const item = sampleMenuItems.find(item => item.id === req.params.id);
    if (!item) {
      return res.status(404).json({ error: 'Menu item not found' });
    }
    res.json(item);
  } catch (error) {
    console.error('Error fetching menu item:', error);
    res.status(500).json({ error: 'Failed to fetch menu item' });
  }
});

// POST /api/menu - Add new menu item (admin only)
router.post('/', async (req, res) => {
  try {
    // For demo purposes, just return success
    res.status(201).json({ message: 'Menu item added successfully', item: req.body });
  } catch (error) {
    console.error('Error adding menu item:', error);
    res.status(500).json({ error: 'Failed to add menu item' });
  }
});

module.exports = router;
