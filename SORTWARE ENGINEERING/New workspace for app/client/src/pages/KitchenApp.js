
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { CartProvider } from '../context/CartContext';
import { AuthProvider } from '../context/AuthContext';
import { NotificationProvider } from '../context/NotificationContext';
import Home from './Home';
import Menu from './Menu';
import MenuEnhanced from './Menu_Enhanced';
import MenuOriginalEnhanced from './Menu_Original_Enhanced';
import Cart from './Cart';
import CartEnhanced from './Cart_Enhanced';
import CartOriginalEnhanced from './Cart_Original_Enhanced';
import Profile from './Profile';
import ProfileOriginalEnhanced from './Profile_Original_Enhanced';
import Login from './Login';
import OrderHistory from './OrderHistory';
import Admin from './Admin';
import Navbar from '../components/Navbar';
import FloatingButtons from '../components/FloatingButtons';
import ProtectedRoute from '../components/ProtectedRoute';

// Define the backend server URL for sockets and API calls
const SOCKET_SERVER_URL = 'http://localhost:5000';

const KitchenApp = () => {
  return (
    <AuthProvider>
      <NotificationProvider>
        <CartProvider>
          <div className="kitchen-app">
            <Navbar />
            <main className="main-content">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/menu" element={<MenuOriginalEnhanced />} />
                <Route path="/menu-enhanced" element={<MenuEnhanced />} />
                <Route path="/menu-classic" element={<Menu />} />
                <Route path="/cart" element={<CartOriginalEnhanced />} />
                <Route path="/cart-enhanced" element={<CartEnhanced />} />
                <Route path="/cart-classic" element={<Cart />} />
                <Route path="/login" element={<Login />} />
                <Route 
                  path="/profile" 
                  element={
                    <ProtectedRoute>
                      <ProfileOriginalEnhanced />
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/profile-classic" 
                  element={
                    <ProtectedRoute>
                      <Profile />
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/orders" 
                  element={
                    <ProtectedRoute>
                      <OrderHistory />
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/admin" 
                  element={
                    <ProtectedRoute>
                      <Admin />
                    </ProtectedRoute>
                  }
                />
                <Route path="*" element={<div className="not-found">404 - Page Not Found</div>} />
              </Routes>
            </main>
            <FloatingButtons />
          </div>
        </CartProvider>
      </NotificationProvider>
    </AuthProvider>
  );
};

export default KitchenApp;
