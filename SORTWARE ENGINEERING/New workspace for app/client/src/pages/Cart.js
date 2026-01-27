import React from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../context/CartContext';

const Cart = () => {
  const { cart, removeFromCart, updateQuantity, getTotalPrice, clearCart } = useCart();

  if (cart.length === 0) {
    return (
      <div className="page cart-page">
        <div className="container">
          <h1>Shopping Cart</h1>
          <div className="empty-cart">
            <h2>Your cart is empty</h2>
            <p>Add some delicious items from our menu!</p>
            <Link to="/menu" className="btn btn-primary">
              Browse Menu
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page cart-page">
      <div className="container">
        <h1>Shopping Cart</h1>
        
        <div className="cart-items">
          {cart.map((item) => (
            <div key={item.id} className="cart-item">
              <div className="item-info">
                <h3>{item.name}</h3>
                <p>{item.description}</p>
                <p className="item-price">R{item.price.toFixed(2)}</p>
              </div>
              
              <div className="quantity-controls">
                <button 
                  onClick={() => updateQuantity(item.id, item.quantity - 1)}
                  className="quantity-btn"
                  disabled={item.quantity <= 1}
                >
                  -
                </button>
                <span className="quantity">{item.quantity}</span>
                <button 
                  onClick={() => updateQuantity(item.id, item.quantity + 1)}
                  className="quantity-btn"
                >
                  +
                </button>
              </div>
              
              <div className="item-total">
                <p>R{(item.price * item.quantity).toFixed(2)}</p>
                <button 
                  onClick={() => removeFromCart(item.id)}
                  className="remove-btn"
                >
                  🗑️ Remove
                </button>
              </div>
            </div>
          ))}
        </div>
        
        <div className="cart-summary">
          <div className="total">
            <h2>Total: R{getTotalPrice().toFixed(2)}</h2>
          </div>
          
          <div className="cart-actions">
            <button 
              onClick={clearCart}
              className="btn btn-secondary"
            >
              Clear Cart
            </button>
            <Link to="/checkout" className="btn btn-primary">
              Proceed to Checkout
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;
