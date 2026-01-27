const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const dotenv = require('dotenv');
const helmet = require('helmet');
const morgan = require('morgan');
const path = require('path');

// Import routes
const orderRoutes = require('./routes/orderRoutes');
const menuRoutes = require('./routes/menuRoutes');
const uploadRoutes = require('./routes/uploadRoutes');
const userRoutes = require('./routes/userRoutes');

// Load environment variables
dotenv.config();

const app = express();
const http = require('http').createServer(app);
const { Server } = require('socket.io');
const io = new Server(http, {
  cors: {
    origin: process.env.CLIENT_URL || 'http://localhost:3000',
    methods: ['GET', 'POST'],
    credentials: true
  }
});
const PORT = process.env.PORT || 5000;
// Real-time tracking endpoint
// POST { id, lat, lng }
app.post('/api/track', (req, res) => {
  const { id, lat, lng } = req.body;
  if (!id || typeof lat !== 'number' || typeof lng !== 'number') {
    return res.status(400).json({ error: 'Invalid payload' });
  }
  // Broadcast to all connected clients
  io.emit('locationUpdate', { id, lat, lng });
  res.json({ status: 'ok' });
});

// Socket.io connection
io.on('connection', (
  
  socket) => {
  console.log('A client connected for real-time tracking:', socket.id);
  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

// Database connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/buroko-kitchen')
  .then(() => console.log('📁 Connected to MongoDB'))
  .catch(err => console.error('❌ MongoDB connection error:', err));

// Middleware
app.use(helmet());
app.use(morgan('combined'));
app.use(cors({
  origin: process.env.CLIENT_URL || 'http://localhost:3000',
  credentials: true
}));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Static files
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// Routes
app.use('/api/orders', orderRoutes);
app.use('/api/menu', menuRoutes);
app.use('/api/upload', uploadRoutes);
app.use('/api/users', userRoutes);

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    message: 'Buroko\'s Kitchen API is running',
    timestamp: new Date().toISOString()
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('❌ Error:', err.stack);
  res.status(500).json({ 
    error: 'Something went wrong!',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Internal server error'
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

http.listen(PORT, () => {
  console.log(`🚀 Server running with real-time tracking on port ${PORT}`);
  console.log(`🌐 Environment: ${process.env.NODE_ENV || 'development'}`);
});
