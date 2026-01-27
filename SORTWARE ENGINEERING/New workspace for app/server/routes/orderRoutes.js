const express = require('express');
const router = express.Router();
const { body, validationResult } = require('express-validator');
const Order = require('../models/Order');

// Validation middleware
const validateOrder = [
  body('customerInfo.name').notEmpty().trim().withMessage('Customer name is required'),
  body('customerInfo.email').isEmail().normalizeEmail().withMessage('Valid email is required'),
  body('customerInfo.phone').notEmpty().trim().withMessage('Phone number is required'),
  body('items').isArray({ min: 1 }).withMessage('At least one item is required'),
  body('totalAmount').isNumeric({ min: 0 }).withMessage('Valid total amount is required')
];

// GET /api/orders - Get all orders (admin only)
router.get('/', async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const status = req.query.status;
    const startIndex = (page - 1) * limit;

    let query = {};
    if (status) {
      query.status = status;
    }

    const orders = await Order.find(query)
      .sort({ createdAt: -1 })
      .limit(limit)
      .skip(startIndex)
      .exec();

    const total = await Order.countDocuments(query);

    res.json({
      orders,
      currentPage: page,
      totalPages: Math.ceil(total / limit),
      totalOrders: total
    });
  } catch (error) {
    console.error('Error fetching orders:', error);
    res.status(500).json({ error: 'Failed to fetch orders' });
  }
});

// GET /api/orders/:id - Get specific order
router.get('/:id', async (req, res) => {
  try {
    const order = await Order.findById(req.params.id);
    
    if (!order) {
      return res.status(404).json({ error: 'Order not found' });
    }

    res.json(order);
  } catch (error) {
    console.error('Error fetching order:', error);
    res.status(500).json({ error: 'Failed to fetch order' });
  }
});

// POST /api/orders - Create new order
router.post('/', validateOrder, async (req, res) => {
  try {
    // Check for validation errors
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ 
        error: 'Validation failed', 
        details: errors.array() 
      });
    }

    const orderData = req.body;
    
    // Calculate estimated delivery time (45 minutes from now)
    const estimatedDeliveryTime = new Date();
    estimatedDeliveryTime.setMinutes(estimatedDeliveryTime.getMinutes() + 45);
    
    const newOrder = new Order({
      ...orderData,
      estimatedDeliveryTime
    });

    const savedOrder = await newOrder.save();

    res.status(201).json({ 
      message: 'Order placed successfully!', 
      order: savedOrder,
      orderNumber: savedOrder.orderNumber
    });
  } catch (error) {
    console.error('Error creating order:', error);
    res.status(500).json({ error: 'Failed to create order' });
  }
});

// PUT /api/orders/:id/status - Update order status
router.put('/:id/status', async (req, res) => {
  try {
    const { status } = req.body;
    
    const validStatuses = ['pending', 'confirmed', 'preparing', 'ready', 'out-for-delivery', 'delivered', 'cancelled'];
    if (!validStatuses.includes(status)) {
      return res.status(400).json({ error: 'Invalid status' });
    }

    const order = await Order.findByIdAndUpdate(
      req.params.id,
      { status },
      { new: true }
    );

    if (!order) {
      return res.status(404).json({ error: 'Order not found' });
    }

    res.json({ message: 'Order status updated', order });
  } catch (error) {
    console.error('Error updating order status:', error);
    res.status(500).json({ error: 'Failed to update order status' });
  }
});

// GET /api/orders/customer/:email - Get orders for specific customer
router.get('/customer/:email', async (req, res) => {
  try {
    const orders = await Order.find({ 'customerInfo.email': req.params.email })
      .sort({ createdAt: -1 })
      .exec();

    res.json(orders);
  } catch (error) {
    console.error('Error fetching customer orders:', error);
    res.status(500).json({ error: 'Failed to fetch customer orders' });
  }
});

// DELETE /api/orders/:id - Cancel order (within 5 minutes of placing)
router.delete('/:id', async (req, res) => {
  try {
    const order = await Order.findById(req.params.id);
    
    if (!order) {
      return res.status(404).json({ error: 'Order not found' });
    }

    // Check if order can be cancelled (within 5 minutes and not yet confirmed)
    const timeDiff = Date.now() - order.createdAt.getTime();
    const fiveMinutes = 5 * 60 * 1000;

    if (timeDiff > fiveMinutes || order.status !== 'pending') {
      return res.status(400).json({ 
        error: 'Order cannot be cancelled. Contact restaurant directly.' 
      });
    }

    order.status = 'cancelled';
    await order.save();

    res.json({ message: 'Order cancelled successfully', order });
  } catch (error) {
    console.error('Error cancelling order:', error);
    res.status(500).json({ error: 'Failed to cancel order' });
  }
});

module.exports = router;
