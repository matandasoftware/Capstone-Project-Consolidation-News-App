import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useNotification } from '../context/NotificationContext';

const CartEnhanced = () => {
  const { cart, removeFromCart, updateQuantity, getTotalPrice, clearCart, getTotalItems } = useCart();
  const { showSuccess, showInfo } = useNotification();
  const [isCheckingOut, setIsCheckingOut] = useState(false);

  const handleQuantityChange = (itemId, newQuantity, itemName) => {
    if (newQuantity === 0) {
      removeFromCart(itemId);
      showInfo(`${itemName} removed from cart`);
    } else {
      updateQuantity(itemId, newQuantity);
    }
  };

  const handleRemoveItem = (item) => {
    removeFromCart(item.id);
    showInfo(`${item.name} removed from cart`);
  };

  const handleClearCart = () => {
    if (window.confirm('Are you sure you want to clear your cart?')) {
      clearCart();
      showSuccess('Cart cleared successfully');
    }
  };

  const handleCheckout = () => {
    setIsCheckingOut(true);
    // Simulate checkout process
    setTimeout(() => {
      showSuccess('Order placed successfully!');
      clearCart();
      setIsCheckingOut(false);
    }, 2000);
  };

  const deliveryFee = 25.00;
  const subtotal = getTotalPrice();
  const finalTotal = subtotal + deliveryFee;

  if (cart.length === 0) {
    return (
      <div className="page cart-page-enhanced">
        <div className="container">
          <div className="cart-header">
            <h1>🛒 Shopping Cart</h1>
            <p>Your delicious orders await</p>
          </div>
          
          <div className="empty-cart">
            <div className="empty-cart-icon">🍽️</div>
            <h2>Your cart is empty</h2>
            <p>Looks like you haven't added anything to your cart yet.</p>
            <p>Start exploring our delicious menu!</p>
            <Link to="/kitchen/menu" className="btn-explore-menu">
              <span>🍔</span>
              Explore Menu
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page cart-page-enhanced">
      <div className="container">
        <div className="cart-header">
          <h1>🛒 Shopping Cart</h1>
          <p>{getTotalItems()} item{getTotalItems() !== 1 ? 's' : ''} in your cart</p>
        </div>
        
        <div className="cart-content">
          <div className="cart-items-section">
            <div className="cart-items-header">
              <h3>Your Items</h3>
              <button 
                onClick={handleClearCart}
                className="clear-cart-btn"
                disabled={isCheckingOut}
              >
                🗑️ Clear All
              </button>
            </div>

            <div className="cart-items-list">
              {cart.map((item) => (
                <div key={`${item.id}-${Math.random()}`} className="cart-item-enhanced">
                  <div className="item-image">
                    <img 
                      src={item.image || '/images/menu/placeholder.jpg'} 
                      alt={item.name}
                      onError={(e) => {
                        e.target.src = '/images/menu/placeholder.jpg';
                      }}
                    />
                  </div>
                  
                  <div className="item-details">
                    <h4>{item.name}</h4>
                    <p className="item-description">{item.description}</p>
                    
                    <div className="item-meta">
                      {item.spicy && <span className="meta-tag spicy">🌶️ Spicy</span>}
                      {item.vegetarian && <span className="meta-tag veggie">🌱 Veggie</span>}
                      {item.popular && <span className="meta-tag popular">🔥 Popular</span>}
                    </div>
                    
                    <div className="item-price-info">
                      <span className="unit-price">R{item.price.toFixed(2)} each</span>
                    </div>
                  </div>
                  
                  <div className="item-actions">
                    <div className="quantity-controls-enhanced">
                      <button 
                        onClick={() => handleQuantityChange(item.id, item.quantity - 1, item.name)}
                        className="qty-btn minus"
                        disabled={isCheckingOut}
                      >
                        -
                      </button>
                      <span className="quantity-display">{item.quantity}</span>
                      <button 
                        onClick={() => handleQuantityChange(item.id, item.quantity + 1, item.name)}
                        className="qty-btn plus"
                        disabled={isCheckingOut}
                      >
                        +
                      </button>
                    </div>
                    
                    <div className="item-total-price">
                      <strong>R{(item.price * item.quantity).toFixed(2)}</strong>
                    </div>
                    
                    <button 
                      onClick={() => handleRemoveItem(item)}
                      className="remove-item-btn"
                      disabled={isCheckingOut}
                      title="Remove item"
                    >
                      ❌
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          <div className="cart-summary-section">
            <div className="cart-summary-enhanced">
              <h3>Order Summary</h3>
              
              <div className="summary-line">
                <span>Subtotal ({getTotalItems()} item{getTotalItems() !== 1 ? 's' : ''})</span>
                <span>R{subtotal.toFixed(2)}</span>
              </div>
              
              <div className="summary-line">
                <span>Delivery Fee</span>
                <span>R{deliveryFee.toFixed(2)}</span>
              </div>
              
              <div className="summary-line discount">
                <span>First Order Discount</span>
                <span className="discount-amount">-R5.00</span>
              </div>
              
              <hr className="summary-divider" />
              
              <div className="summary-line total">
                <span>Total</span>
                <span>R{(finalTotal - 5).toFixed(2)}</span>
              </div>
              
              <div className="delivery-info">
                <div className="delivery-item">
                  <span className="delivery-icon">🚚</span>
                  <div>
                    <strong>Delivery Time</strong>
                    <p>20-30 minutes</p>
                  </div>
                </div>
                
                <div className="delivery-item">
                  <span className="delivery-icon">📍</span>
                  <div>
                    <strong>Delivery Address</strong>
                    <p>Current Location</p>
                  </div>
                </div>
              </div>
              
              <div className="checkout-actions">
                <Link to="/kitchen/menu" className="continue-shopping-btn">
                  ← Continue Shopping
                </Link>
                
                <button 
                  onClick={handleCheckout}
                  className="checkout-btn"
                  disabled={isCheckingOut}
                >
                  {isCheckingOut ? (
                    <span>
                      <span className="loading-spinner"></span>
                      Processing...
                    </span>
                  ) : (
                    <span>
                      🛒 Proceed to Checkout
                    </span>
                  )}
                </button>
              </div>
              
              <div className="payment-methods">
                <p>We accept:</p>
                <div className="payment-icons">
                  <span>💳</span>
                  <span>📱</span>
                  <span>💰</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CartEnhanced;
