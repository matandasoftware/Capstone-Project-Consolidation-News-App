import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useNotification } from '../context/NotificationContext';

const CartOriginalEnhanced = () => {
  const { cart, removeFromCart, clearCart, getTotalItems } = useCart();
  const { showSuccess, showInfo } = useNotification();
  const navigate = useNavigate();

  const [profile, setProfile] = useState(null);
  const [deliveryTime, setDeliveryTime] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [isCheckingOut, setIsCheckingOut] = useState(false);

  // Calculate totals
  const subtotal = cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  const deliveryFee = 14.00;
  const finalTotal = subtotal + deliveryFee;
  const reference = `BUR-${Math.floor(Math.random() * 900000 + 100000)}`;

  // Helper to format date to "HH:mm"
  const formatTime = (date) => date.toTimeString().slice(0, 5);

  // Generate suggested delivery windows (3 options)
  const generateSuggestions = () => {
    const now = new Date();
    const windows = [
      [60, 75],
      [75, 90],
      [90, 105],
    ];

    return windows.map(([startMin, endMin]) => {
      const start = new Date(now.getTime() + startMin * 60000);
      const end = new Date(now.getTime() + endMin * 60000);
      return `${formatTime(start)} - ${formatTime(end)}`;
    });
  };

  // On mount, load profile and generate suggestions
  useEffect(() => {
    const stored = localStorage.getItem('customerProfile');
    if (stored) {
      const parsed = JSON.parse(stored);
      setProfile(parsed);

      const newSuggestions = generateSuggestions();
      setSuggestions(newSuggestions);

      if (parsed.time && newSuggestions.includes(parsed.time)) {
        setDeliveryTime(parsed.time);
      } else {
        setDeliveryTime(newSuggestions[0]);
      }
    }
  }, []);

  const handleWhatsAppOrder = async () => {
    if (!profile) {
      showInfo('Please complete your profile first');
      navigate('/kitchen/profile');
      return;
    }

    setIsCheckingOut(true);

    // Create WhatsApp message with original format
    const message = encodeURIComponent(
      `🍟 *Buroko Order* 🍟\n\n` +
      cart.map((item) => `• ${item.name} x${item.quantity} (R${(item.price * item.quantity).toFixed(2)})`).join('\n') +
      `\n\n💰 *Subtotal:* R${subtotal.toFixed(2)}` +
      `\n🚚 *Delivery:* R${deliveryFee.toFixed(2)}` +
      `\n💵 *Total:* R${finalTotal.toFixed(2)}` +
      `\n👤 *Name:* ${profile.name}` +
      `\n📞 *Phone:* ${profile.phone}` +
      `\n🏠 *Address:* ${profile.address}` +
      `\n⏰ *Delivery Time:* ${deliveryTime}` +
      `\n\n💳 *Capitec EFT Payment Info:*\nAccount: 1573874570\nBank: Capitec\nRef: ${reference}`
    );

    // Open WhatsApp
    window.open(`https://wa.me/27815468207?text=${message}`, '_blank');

    try {
      // Simulate saving order (replace with actual Firebase if available)
      const order = {
        ...profile,
        items: cart,
        subtotal,
        deliveryFee,
        total: finalTotal,
        deliveryTime,
        reference,
        created: new Date().toISOString(),
      };

      // Save to localStorage as backup
      const existingOrders = JSON.parse(localStorage.getItem('orders') || '[]');
      existingOrders.push(order);
      localStorage.setItem('orders', JSON.stringify(existingOrders));

      setTimeout(() => {
        showSuccess("Order sent via WhatsApp! Please complete payment.");
        clearCart();
        setIsCheckingOut(false);
        navigate('/kitchen/');
      }, 2000);
    } catch (err) {
      console.error("Order failed:", err);
      showInfo("Could not save order, but WhatsApp message sent.");
      setIsCheckingOut(false);
    }
  };

  function handleRemoveItem(index) {
    const item = cart[index];
    removeFromCart(index);
    showInfo(`${item.name} removed from cart`);
  }

  const handleClearCart = () => {
    if (window.confirm('Are you sure you want to clear your cart?')) {
      clearCart();
      showSuccess('Cart cleared successfully');
    }
  };

  if (cart.length === 0) {
    return (
      <div className="page cart-page-enhanced">
        <div className="container">
          <div className="cart-header">
            <h1>🛒 Your Cart</h1>
            <p>Start building your order</p>
          </div>
          
          <div className="empty-cart">
            <div className="empty-cart-icon">🍽️</div>
            <h2>Your cart is empty</h2>
            <p>Browse our delicious menu and add items to get started!</p>
            <Link to="/kitchen/menu" className="btn-explore-menu">
              <span>🍔</span>
              Browse Menu
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
          <h1>🛒 Your Cart</h1>
          <p>{getTotalItems()} item{getTotalItems() !== 1 ? 's' : ''} • R{finalTotal.toFixed(2)} total</p>
        </div>
        
        <div className="cart-content">
          <div className="cart-items-section">
            <div className="cart-items-header">
              <h3>Order Items</h3>
              <button 
                onClick={handleClearCart}
                className="clear-cart-btn"
                disabled={isCheckingOut}
              >
                🗑️ Clear All
              </button>
            </div>

            <div className="cart-items-list">
              {cart.map((item, index) => (
                <div key={`${item.id}-${index}`} className="cart-item-enhanced original-style">
                  <div className="item-image">
                    <img 
                      src={item.image || '/images/logos/burokos-kitchen-logo.jpg'} 
                      alt={item.name}
                      onError={(e) => {
                        e.target.src = '/images/logos/burokos-kitchen-logo.jpg';
                      }}
                    />
                  </div>
                  
                  <div className="item-details">
                    <h4>{item.name}</h4>
                    <p className="item-description">{item.description}</p>
                    
                    <div className="item-price-info">
                      <span className="unit-price">R{item.price.toFixed(2)} each</span>
                      {item.quantity > 1 && (
                        <span className="quantity-info"> × {item.quantity}</span>
                      )}
                    </div>
                  </div>
                  
                  <div className="item-actions">
                    <div className="item-total-price">
                      <strong>R{(item.price * item.quantity).toFixed(2)}</strong>
                    </div>
                    
                    <button 
                      onClick={() => handleRemoveItem(index)}
                      className="remove-item-btn"
                      disabled={isCheckingOut}
                      title="Remove item"
                    >
                      Remove
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
                <span>Delivery Fee (Thohoyandou)</span>
                <span>R{deliveryFee.toFixed(2)}</span>
              </div>
              
              <hr className="summary-divider" />
              
              <div className="summary-line total">
                <span>Total</span>
                <span>R{finalTotal.toFixed(2)}</span>
              </div>

              {/* Delivery Time Selection */}
              <div className="delivery-section">
                <h4>📅 Delivery Time</h4>
                
                {suggestions.length > 0 && (
                  <div className="time-suggestions">
                    <p>Suggested times:</p>
                    <div className="time-buttons">
                      {suggestions.map((slot) => (
                        <button
                          key={slot}
                          onClick={() => setDeliveryTime(slot)}
                          className={`time-slot-btn ${deliveryTime === slot ? 'active' : ''}`}
                          disabled={isCheckingOut}
                        >
                          {slot}
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                <div className="custom-time">
                  <label htmlFor="deliveryTime">Or enter custom time:</label>
                  <input
                    id="deliveryTime"
                    type="text"
                    value={deliveryTime}
                    onChange={(e) => setDeliveryTime(e.target.value)}
                    placeholder="e.g., 14:00 - 15:00"
                    disabled={isCheckingOut}
                  />
                </div>
              </div>

              {/* Profile Information */}
              {profile && (
                <div className="profile-section">
                  <h4>👤 Delivery Details</h4>
                  <div className="profile-info">
                    <p><strong>Name:</strong> {profile.name}</p>
                    <p><strong>Phone:</strong> {profile.phone}</p>
                    <p><strong>Address:</strong> {profile.address}</p>
                  </div>
                  <Link to="/kitchen/profile" className="edit-profile-btn">
                    ✏️ Edit Details
                  </Link>
                </div>
              )}

              {/* Payment Information */}
              <div className="payment-section">
                <h4>💳 Payment Info</h4>
                <div className="payment-details">
                  <p><strong>Bank:</strong> Capitec</p>
                  <p><strong>Account:</strong> 1573874570</p>
                  <p><strong>Reference:</strong> {reference}</p>
                </div>
                <p className="payment-note">
                  📱 Complete EFT payment and confirm via WhatsApp
                </p>
              </div>
              
              <div className="checkout-actions">
                <Link to="/kitchen/menu" className="continue-shopping-btn">
                  ← Continue Shopping
                </Link>
                
                <button 
                  onClick={handleWhatsAppOrder}
                  className="checkout-btn whatsapp-btn"
                  disabled={isCheckingOut || !profile}
                >
                  {isCheckingOut ? (
                    <span>
                      <span className="loading-spinner"></span>
                      Sending...
                    </span>
                  ) : (
                    <span>
                      📱 Send Order via WhatsApp
                    </span>
                  )}
                </button>

                {!profile && (
                  <Link to="/kitchen/profile" className="profile-required-btn">
                    👤 Complete Profile First
                  </Link>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CartOriginalEnhanced;
