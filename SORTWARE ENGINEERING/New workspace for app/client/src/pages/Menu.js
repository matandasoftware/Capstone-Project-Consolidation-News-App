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
    <div className="menu-page">
      <div className="menu-header">
        <h1>Our Menu</h1>
        <p>Choose from our selection of fresh, delicious meals</p>
      </div>

      <div className="menu-controls">
        <div className="search-bar">
          <div className="search-icon">🔍</div>
          <input
            type="text"
            placeholder="Search menu items..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="category-filter">
          <div className="filter-icon">🔽</div>
          <select 
            value={selectedCategory} 
            onChange={(e) => setSelectedCategory(e.target.value)}
          >
            {categories.map(category => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="menu-grid">
        {filteredItems.map((item) => (
          <div key={item.id} className={`menu-card ${item.popular ? 'popular' : ''}`}>
            {item.popular && <span className="popular-badge">Popular</span>}
            
            <div className="card-image">
              <img 
                src={item.image} 
                alt={item.name}
                onError={(e) => {
                  e.target.src = '/images/placeholder.jpg';
                }}
              />
            </div>
            
            <div className="card-content">
              <h3 className="card-title">{item.name}</h3>
              <p className="card-description">{item.description}</p>
              <div className="card-footer">
                <span className="card-price">R{item.price.toFixed(2)}</span>
                <button 
                  className="add-to-cart-btn"
                  onClick={() => handleAddToCart(item)}
                  aria-label={`Add ${item.name} to cart`}
                >
                  <span>➕</span>
                  Add to Cart
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredItems.length === 0 && (
        <div className="no-items">
          <p>No items found matching your search.</p>
        </div>
      )}

      {getTotalItems() > 0 && (
        <Link to="/cart" className="floating-cart-button">
          <span>🛒</span>
          <span className="cart-count">{getTotalItems()}</span>
          View Cart (R{cart.reduce((total, item) => total + (item.price * item.quantity), 0).toFixed(2)})
        </Link>
      )}
    </div>
  );
};

export default Menu;
