import React, { useState } from 'react';
import { useCart } from '../context/CartContext';
import { useNotification } from '../context/NotificationContext';
import '../styles/menu-responsive.css';

const MenuOriginalEnhanced = () => {
  const { addToCart } = useCart();
  const { showSuccess } = useNotification();
  const [selectedCategory, setSelectedCategory] = useState('all');

  // Original menu items from Buroko's Kitchen
  const menuItems = [
    {
      id: 1,
      name: 'Siphos',
      price: 21.90,
      description: 'Chips, polony, lettuce & half viana',
      category: 'burgers',
      image: '/images/menu/siphos.svg',
      isPopular: true
    },
    {
      id: 2,
      name: 'Brokolos',
      price: 34.00,
      description: 'Chips, polony, lettuce, cheese, full viana & half russian',
      category: 'burgers',
      image: '/images/menu/placeholder.svg',
      isPopular: true
    },
    {
      id: 3,
      name: 'Letse',
      price: 42.00,
      description: 'Chips, polony, lettuce, cheese, cucumber, full viana & russian',
      category: 'burgers',
      image: '/images/menu/placeholder.svg'
    },
    {
      id: 4,
      name: 'Enzo',
      price: 52.00,
      description: 'Chips, polony, lettuce, cheese, full viana, russian + patty',
      category: 'burgers',
      image: '/images/menu/placeholder.svg',
      isPopular: true
    },
    {
      id: 5,
      name: 'Vruuupaaa!',
      price: 40.00,
      description: 'Wrap with chips, lettuce, tomato, polony, russian, viana, cheese',
      category: 'wraps',
      image: '/images/menu/vruuupaaa.svg'
    },
    {
      id: 6,
      name: 'Ayoba',
      price: 65.00,
      description: 'Wrap + egg + patty',
      category: 'wraps',
      image: '/images/menu/placeholder.svg'
    },
    {
      id: 7,
      name: 'Buroko Combo',
      price: 50.00,
      description: 'Chips, 3 russians, brown bread, atchar, polony',
      category: 'combos',
      image: '/images/menu/buroko-combo.svg',
      isPopular: true
    }
  ];

  const categories = [
    { id: 'all', name: 'All Items', icon: '🍽️' },
    { id: 'burgers', name: 'Burgers', icon: '�' },
    { id: 'wraps', name: 'Wraps', icon: '�' },
    { id: 'combos', name: 'Combos', icon: '�' }
  ];

  const filteredItems = selectedCategory === 'all' 
    ? menuItems 
    : menuItems.filter(item => item.category === selectedCategory);

  const handleAddToCart = (item) => {
    addToCart(item);
    showSuccess(`${item.name} added to cart!`);
  };

  return (
    <div className="menu-page-enhanced">
      <div className="menu-header">
        <h1>🍽️ Buroko's Kitchen Menu</h1>
        <p>Authentic South African flavors, crafted with love</p>
      </div>

      <div className="menu-container">
        {/* Categories Filter */}
        <div className="categories-section">
          <h3>Browse by Category</h3>
          <div className="categories-grid">
            {categories.map((category) => (
              <button
                key={category.id}
                className={`category-btn ${selectedCategory === category.id ? 'active' : ''}`}
                onClick={() => setSelectedCategory(category.id)}
              >
                <span className="category-icon">{category.icon}</span>
                <span className="category-name">{category.name}</span>
                <span className="item-count">
                  ({category.id === 'all' ? menuItems.length : menuItems.filter(item => item.category === category.id).length})
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Menu Items */}
        <div className="menu-items-section">
          <div className="section-header">
            <h2>
              {categories.find(cat => cat.id === selectedCategory)?.icon} {' '}
              {categories.find(cat => cat.id === selectedCategory)?.name}
            </h2>
            <p>{filteredItems.length} items available</p>
          </div>

          <div className="menu-grid">
            {filteredItems.map((item) => (
              <div key={item.id} className={`menu-item-card original-style ${item.isPopular ? 'popular' : ''}`}>
                {item.isPopular && (
                  <div className="popular-badge">
                    ⭐ Popular
                  </div>
                )}
                
                <div className="item-image">
                  <img 
                    src={item.image}
                    alt={item.name}
                    onError={(e) => {
                      e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjZjVmNWY1Ii8+CjxwYXRoIGQ9Ik0xMDAgNTBMMTUwIDEwMEgxMDBWMTUwSDUwVjEwMEgxMDBaIiBmaWxsPSIjY2NjIi8+Cjx0ZXh0IHg9IjEwMCIgeT0iMTgwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiM5OTkiPkJ1cm9rbyBEaXNoPC90ZXh0Pgo8L3N2Zz4K';
                    }}
                  />
                  <div className="item-overlay">
                    <button 
                      className="quick-add-btn"
                      onClick={() => handleAddToCart(item)}
                    >
                      ➕ Quick Add
                    </button>
                  </div>
                </div>

                <div className="item-content">
                  <div className="item-header">
                    <h3>{item.name}</h3>
                    <span className="price">R{item.price.toFixed(2)}</span>
                  </div>
                  
                  <p className="description">{item.description}</p>
                  
                  <div className="item-footer">
                    <span className="category-tag">
                      {categories.find(cat => cat.id === item.category)?.icon} {' '}
                      {categories.find(cat => cat.id === item.category)?.name}
                    </span>
                    
                    <button 
                      className="add-to-cart-btn"
                      onClick={() => handleAddToCart(item)}
                    >
                      Add to Cart
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Delivery Info */}
        <div className="delivery-info-section">
          <h3>🚚 Delivery Information</h3>
          <div className="delivery-details">
            <div className="delivery-item">
              <span className="icon">📍</span>
              <div>
                <strong>Delivery Areas</strong>
                <p>Johannesburg Central, Soweto, Alexandra, Randburg</p>
              </div>
            </div>
            <div className="delivery-item">
              <span className="icon">⏰</span>
              <div>
                <strong>Delivery Time</strong>
                <p>30-45 minutes during peak hours</p>
              </div>
            </div>
            <div className="delivery-item">
              <span className="icon">💳</span>
              <div>
                <strong>Payment</strong>
                <p>Capitec EFT, Cash on Delivery</p>
              </div>
            </div>
            <div className="delivery-item">
              <span className="icon">📱</span>
              <div>
                <strong>Order via WhatsApp</strong>
                <p>Quick and easy ordering through WhatsApp</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MenuOriginalEnhanced;
