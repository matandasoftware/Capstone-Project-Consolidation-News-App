import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useNotification } from '../context/NotificationContext';
import LoadingSpinner from '../components/LoadingSpinner';

const Menu = () => {
  const { cart, addToCart, getTotalItems } = useCart();
  const { showSuccess, showError } = useNotification();
  const [menuItems, setMenuItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [sortBy, setSortBy] = useState('name');
  const [selectedItem, setSelectedItem] = useState(null);
  const [itemQuantity, setItemQuantity] = useState({});

  // Enhanced menu data with more details
  const sampleMenuItems = [
    {
      id: 1,
      name: 'Ayoba',
      description: 'Wrap + egg + patty',
      longDescription: 'Our signature wrap featuring a perfectly cooked egg, seasoned beef patty, fresh lettuce, tomatoes, and our special sauce wrapped in a soft tortilla.',
      price: 65,
      category: 'wraps',
      image: '/images/menu/ayoba.jpg',
      popular: true,
      spicy: false,
      vegetarian: false,
      prepTime: '5-8 mins',
      calories: 450,
      ingredients: ['Tortilla wrap', 'Beef patty', 'Egg', 'Lettuce', 'Tomato', 'Special sauce']
    },
    {
      id: 2,
      name: 'Siphos',
      description: 'Chips, polony, lettuce & half loaf',
      longDescription: 'A hearty combo meal with golden crispy chips, sliced polony, fresh lettuce, and half a loaf of our freshly baked bread.',
      price: 50,
      category: 'combos',
      image: '/images/menu/siphos.jpg',
      popular: false,
      spicy: false,
      vegetarian: false,
      prepTime: '8-10 mins',
      calories: 520,
      ingredients: ['Chips', 'Polony', 'Lettuce', 'Half loaf bread']
    },
    {
      id: 3,
      name: 'Russian Special',
      description: 'Chips, 3 russians, brown bread, atchar, polony',
      longDescription: 'Our most popular combo! Crispy chips, three grilled russian sausages, brown bread, spicy atchar, and sliced polony for the ultimate satisfaction.',
      price: 75,
      category: 'combos',
      image: '/images/menu/russian-special.jpg',
      popular: true,
      spicy: true,
      vegetarian: false,
      prepTime: '10-12 mins',
      calories: 680,
      ingredients: ['Chips', 'Russian sausages (3)', 'Brown bread', 'Atchar', 'Polony']
    },
    {
      id: 4,
      name: 'Chicken Wrap',
      description: 'Grilled chicken, lettuce, tomato, mayo',
      longDescription: 'Tender grilled chicken breast with crisp lettuce, fresh tomatoes, and creamy mayonnaise wrapped in a soft tortilla.',
      price: 45,
      category: 'wraps',
      image: '/images/menu/chicken-wrap.jpg',
      popular: false,
      spicy: false,
      vegetarian: false,
      prepTime: '6-8 mins',
      calories: 380,
      ingredients: ['Tortilla wrap', 'Grilled chicken', 'Lettuce', 'Tomato', 'Mayonnaise']
    },
    {
      id: 5,
      name: 'Beef Burger',
      description: 'Beef patty, cheese, lettuce, tomato, onion',
      longDescription: 'Juicy beef patty with melted cheese, fresh lettuce, ripe tomatoes, and onions on a toasted sesame seed bun.',
      price: 55,
      category: 'burgers',
      image: '/images/menu/beef-burger.jpg',
      popular: true,
      spicy: false,
      vegetarian: false,
      prepTime: '8-10 mins',
      calories: 520,
      ingredients: ['Beef patty', 'Cheese', 'Lettuce', 'Tomato', 'Onion', 'Sesame bun']
    },
    {
      id: 6,
      name: 'Veggie Wrap',
      description: 'Mixed vegetables, hummus, lettuce, tomato',
      longDescription: 'A healthy option with grilled mixed vegetables, creamy hummus, fresh lettuce, and tomatoes in a whole wheat wrap.',
      price: 40,
      category: 'wraps',
      image: '/images/menu/veggie-wrap.jpg',
      popular: false,
      spicy: false,
      vegetarian: true,
      prepTime: '5-7 mins',
      calories: 320,
      ingredients: ['Whole wheat wrap', 'Mixed vegetables', 'Hummus', 'Lettuce', 'Tomato']
    },
    {
      id: 7,
      name: 'Chips & Gravy',
      description: 'Crispy chips with savory gravy',
      longDescription: 'Golden crispy potato chips served with our homemade savory gravy.',
      price: 25,
      category: 'sides',
      image: '/images/menu/chips-gravy.jpg',
      popular: true,
      spicy: false,
      vegetarian: true,
      prepTime: '3-5 mins',
      calories: 280,
      ingredients: ['Potato chips', 'Gravy sauce']
    },
    {
      id: 8,
      name: 'Chicken Burger',
      description: 'Grilled chicken breast, lettuce, mayo',
      longDescription: 'Succulent grilled chicken breast with fresh lettuce and creamy mayonnaise on a toasted bun.',
      price: 50,
      category: 'burgers',
      image: '/images/menu/chicken-burger.jpg',
      popular: false,
      spicy: false,
      vegetarian: false,
      prepTime: '8-10 mins',
      calories: 480,
      ingredients: ['Chicken breast', 'Lettuce', 'Mayonnaise', 'Bun']
    }
  ];

  const categories = [
    { id: 'all', name: 'All Items' },
    { id: 'wraps', name: 'Wraps' },
    { id: 'combos', name: 'Combos' },
    { id: 'burgers', name: 'Burgers' },
    { id: 'sides', name: 'Sides' }
  ];

  const sortOptions = [
    { value: 'name', label: 'Name A-Z' },
    { value: 'price-low', label: 'Price: Low to High' },
    { value: 'price-high', label: 'Price: High to Low' },
    { value: 'popular', label: 'Most Popular' }
  ];

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setMenuItems(sampleMenuItems);
      setLoading(false);
    }, 1000);
  }, []);

  const getItemQuantity = (itemId) => {
    return itemQuantity[itemId] || 1;
  };

  const updateItemQuantity = (itemId, quantity) => {
    if (quantity < 1) quantity = 1;
    if (quantity > 10) quantity = 10;
    setItemQuantity(prev => ({
      ...prev,
      [itemId]: quantity
    }));
  };

  const handleAddToCart = (item) => {
    const quantity = getItemQuantity(item.id);
    for (let i = 0; i < quantity; i++) {
      addToCart(item);
    }
    showSuccess(`${quantity}x ${item.name} added to cart!`);
    setItemQuantity(prev => ({
      ...prev,
      [item.id]: 1
    }));
  };

  const handleItemClick = (item) => {
    setSelectedItem(item);
  };

  const closeModal = () => {
    setSelectedItem(null);
  };

  const filteredItems = menuItems.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || item.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const sortedItems = [...filteredItems].sort((a, b) => {
    switch (sortBy) {
      case 'price-low':
        return a.price - b.price;
      case 'price-high':
        return b.price - a.price;
      case 'popular':
        return (b.popular ? 1 : 0) - (a.popular ? 1 : 0);
      default:
        return a.name.localeCompare(b.name);
    }
  });

  if (loading) {
    return <LoadingSpinner message="Loading delicious menu items..." />;
  }

  return (
    <div className="page menu-page">
      <div className="container">
        <div className="menu-header">
          <h1>Our Menu</h1>
          <p>Fresh, delicious meals made to order</p>
        </div>

        <div className="search-filters">
          <div className="search-bar-container">
            <input
              type="text"
              placeholder="Search menu items..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-bar"
            />
            <span className="search-icon">🔍</span>
          </div>

          <div className="filter-controls">
            <div className="category-filter">
              {categories.map(category => (
                <button
                  key={category.id}
                  onClick={() => setSelectedCategory(category.id)}
                  className={`category-btn ${selectedCategory === category.id ? 'active' : ''}`}
                >
                  {category.name}
                </button>
              ))}
            </div>

            <div className="sort-filter">
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="sort-select"
              >
                {sortOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        <div className="menu-stats">
          <p>Showing {sortedItems.length} item{sortedItems.length !== 1 ? 's' : ''}</p>
          {getTotalItems() > 0 && (
            <Link to="/kitchen/cart" className="cart-link">
              🛒 Cart ({getTotalItems()})
            </Link>
          )}
        </div>

        <div className="menu-grid">
          {sortedItems.map((item) => (
            <div key={item.id} className="menu-card" onClick={() => handleItemClick(item)}>
              {item.popular && <span className="popular-badge">🔥 Popular</span>}
              
              <div className="menu-card-image">
                <img 
                  src={item.image} 
                  alt={item.name}
                  onError={(e) => {
                    e.target.src = '/images/menu/placeholder.jpg';
                  }}
                />
                <div className="image-overlay">
                  <div className="item-badges">
                    {item.vegetarian && <span className="badge vegetarian">🌱 Veggie</span>}
                    {item.spicy && <span className="badge spicy">🌶️ Spicy</span>}
                  </div>
                </div>
              </div>

              <div className="menu-card-content">
                <div className="item-header">
                  <h3>{item.name}</h3>
                  <span className="price">R{item.price.toFixed(2)}</span>
                </div>
                
                <p className="description">{item.description}</p>
                
                <div className="item-details">
                  <span className="prep-time">⏱️ {item.prepTime}</span>
                  <span className="calories">📊 {item.calories} cal</span>
                </div>

                <div className="card-actions" onClick={(e) => e.stopPropagation()}>
                  <div className="quantity-selector">
                    <button 
                      className="quantity-btn minus"
                      onClick={() => updateItemQuantity(item.id, getItemQuantity(item.id) - 1)}
                    >
                      -
                    </button>
                    <span className="quantity-display">{getItemQuantity(item.id)}</span>
                    <button 
                      className="quantity-btn plus"
                      onClick={() => updateItemQuantity(item.id, getItemQuantity(item.id) + 1)}
                    >
                      +
                    </button>
                  </div>
                  
                  <button 
                    onClick={() => handleAddToCart(item)}
                    className="add-to-cart-btn"
                  >
                    Add R{(item.price * getItemQuantity(item.id)).toFixed(2)}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {sortedItems.length === 0 && (
          <div className="no-results">
            <h3>No items found</h3>
            <p>Try adjusting your search or filter settings</p>
          </div>
        )}
      </div>

      {/* Item Detail Modal */}
      {selectedItem && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="item-modal" onClick={(e) => e.stopPropagation()}>
            <button className="close-modal" onClick={closeModal}>×</button>
            
            <div className="modal-content">
              <div className="modal-image">
                <img src={selectedItem.image} alt={selectedItem.name} />
                <div className="modal-badges">
                  {selectedItem.popular && <span className="badge popular">🔥 Popular</span>}
                  {selectedItem.vegetarian && <span className="badge vegetarian">🌱 Vegetarian</span>}
                  {selectedItem.spicy && <span className="badge spicy">🌶️ Spicy</span>}
                </div>
              </div>
              
              <div className="modal-details">
                <h2>{selectedItem.name}</h2>
                <p className="modal-description">{selectedItem.longDescription}</p>
                
                <div className="modal-info">
                  <div className="info-item">
                    <strong>Price:</strong> R{selectedItem.price.toFixed(2)}
                  </div>
                  <div className="info-item">
                    <strong>Prep Time:</strong> {selectedItem.prepTime}
                  </div>
                  <div className="info-item">
                    <strong>Calories:</strong> {selectedItem.calories}
                  </div>
                </div>

                <div className="ingredients">
                  <h4>Ingredients:</h4>
                  <ul>
                    {selectedItem.ingredients.map((ingredient, index) => (
                      <li key={index}>{ingredient}</li>
                    ))}
                  </ul>
                </div>

                <div className="modal-actions">
                  <div className="quantity-selector">
                    <button 
                      className="quantity-btn minus"
                      onClick={() => updateItemQuantity(selectedItem.id, getItemQuantity(selectedItem.id) - 1)}
                    >
                      -
                    </button>
                    <span className="quantity-display">{getItemQuantity(selectedItem.id)}</span>
                    <button 
                      className="quantity-btn plus"
                      onClick={() => updateItemQuantity(selectedItem.id, getItemQuantity(selectedItem.id) + 1)}
                    >
                      +
                    </button>
                  </div>
                  
                  <button 
                    onClick={() => {
                      handleAddToCart(selectedItem);
                      closeModal();
                    }}
                    className="add-to-cart-btn large"
                  >
                    Add to Cart - R{(selectedItem.price * getItemQuantity(selectedItem.id)).toFixed(2)}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Menu;
