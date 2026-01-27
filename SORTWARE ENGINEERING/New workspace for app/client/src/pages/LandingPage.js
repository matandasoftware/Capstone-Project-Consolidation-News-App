
import React, { useEffect, useRef, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import io from 'socket.io-client';
import { Link } from 'react-router-dom';

// Define the backend server URL for sockets and API calls
const SOCKET_SERVER_URL = 'http://localhost:5000';

// Fix default marker icon issue in Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});



// ...existing code...

// Place the vendors array back where it was originally used, e.g. inside the component or imported from a data file.

const LandingPage = () => {
  // Sample vendors array (restore original vendors section functionality)
  const vendors = [
    {
      id: '1',
      name: "Buroko's Kitchen",
      description: 'Delicious wraps, burgers, and more! Local favorite for fast food.',
      category: 'Food',
      rating: 4.8,
      deliveryTime: '30-40 min',
      deliveryFee: 'R10',
      image: '/images/logos/burokos-kitchen-logo.jpg',
      fallbackImage: '🍔',
      colors: ['#ffb347', '#ffcc33'],
  path: '/kitchen/menu'
    },
    {
      id: '2',
      name: "Thohoyandou Entertainment",
      description: 'Live music, movies, and events for all ages.',
      category: 'Entertainment',
      rating: 4.7,
      deliveryTime: 'N/A',
      deliveryFee: 'N/A',
      image: '',
      fallbackImage: '🎤',
      colors: ['#636e72', '#00b894'],
      path: '#'
    },
    {
      id: '3',
      name: "Poetry Corner",
      description: 'Local poets, open mic nights, and creative workshops.',
      category: 'Poetry',
      rating: 4.9,
      deliveryTime: 'N/A',
      deliveryFee: 'N/A',
      image: '',
      fallbackImage: '�',
      colors: ['#a29bfe', '#fdcb6e'],
      path: '#'
    },
    {
      id: '4',
      name: "GreenMart Groceries",
      description: 'Groceries and essentials delivered to your door.',
      category: 'Groceries',
      rating: 4.6,
      deliveryTime: '1-2 hours',
      deliveryFee: 'R20',
      image: '',
      fallbackImage: '�',
      colors: ['#fdcb6e', '#00b894'],
      path: '#'
    },
    {
      id: '5',
      name: "FunZone Arcade",
      description: 'Arcade games, family fun, and kids parties.',
      category: 'Entertainment',
      rating: 4.5,
      deliveryTime: 'N/A',
      deliveryFee: 'N/A',
      image: '',
      fallbackImage: '🕹️',
      colors: ['#fd79a8', '#636e72'],
      path: '#'
    },
    {
      id: '6',
      name: "Artisan Crafts",
      description: 'Handmade crafts, gifts, and local art.',
      category: 'Crafts',
      rating: 4.7,
      deliveryTime: '2-3 days',
      deliveryFee: 'R15',
      image: '',
      fallbackImage: '🎨',
      colors: ['#00b894', '#fdcb6e'],
      path: '#'
    }
  ];
  // State for location search and map
  const [searchId, setSearchId] = useState('');
  const [searchResult, setSearchResult] = useState(null);
  const [geoLocation, setGeoLocation] = useState(null);
  const [address, setAddress] = useState('');
  const [addressLocation, setAddressLocation] = useState(null);
  const [addressError, setAddressError] = useState('');
  const [positions, setPositions] = useState([]);
  const socketRef = useRef(null);

  // Fetch all positions on mount and listen for real-time updates
  useEffect(() => {
    fetch(`${SOCKET_SERVER_URL}/api/orders/positions`)
      .then(res => res.json())
      .then(data => setPositions(data))
      .catch(() => setPositions([]));
    socketRef.current = io(SOCKET_SERVER_URL);
    socketRef.current.on('positionUpdate', (data) => {
      setPositions(data);
    });
    return () => {
      if (socketRef.current) socketRef.current.disconnect();
    };
  }, []);

  // Handlers
  const handleSearch = () => {
    if (!searchId) {
      setSearchResult(null);
      return;
    }
    const found = positions.find(pos => pos.id === searchId);
    setSearchResult(found || null);
  };

  const handleGeoLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setGeoLocation({ lat: position.coords.latitude, lng: position.coords.longitude });
        },
        () => {
          setGeoLocation(null);
        }
      );
    }
  };

  // Real-time address geolocation as user types
  useEffect(() => {
    if (!address) {
      setAddressLocation(null);
      setAddressError('');
      return;
    }
    const controller = new AbortController();
    const fetchGeo = async () => {
      try {
        const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`, { signal: controller.signal });
        const data = await res.json();
        if (data && data.length > 0) {
          setAddressLocation({ lat: parseFloat(data[0].lat), lng: parseFloat(data[0].lon) });
          setAddressError('');
        } else {
          setAddressLocation(null);
          setAddressError('Address not found');
        }
      } catch (err) {
        if (err.name !== 'AbortError') {
          setAddressLocation(null);
          setAddressError('Error searching address');
        }
      }
    };
    const timeout = setTimeout(fetchGeo, 500); // debounce
    return () => {
      controller.abort();
      clearTimeout(timeout);
    };
  }, [address]);

  // Remove the old handleAddressSearch button

  // Fallback for vendors array
  const vendorsSafe = typeof vendors !== 'undefined' ? vendors : [];

  return (
    <div className="landing-page">
      {/* DEBUG: If you see this, the LandingPage is rendering! */}
      {/* Location Search and Map at the very top */}
      <div style={{ width: '100%', background: '#f8f8f8', padding: '24px 0', marginBottom: 32 }}>
        <div className="container">
          <h2>Location Search</h2>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 12, alignItems: 'center', marginBottom: 16 }}>
            <input
              type="text"
              placeholder="Search by ID..."
              value={searchId}
              onChange={e => setSearchId(e.target.value)}
              style={{ padding: '4px 8px' }}
            />
            <button onClick={handleSearch}>Search by ID</button>
            <button onClick={handleGeoLocation}>Use My Location</button>
            <input
              type="text"
              placeholder="Search by Address..."
              value={address}
              onChange={e => setAddress(e.target.value)}
              style={{ padding: '4px 8px', minWidth: 200 }}
            />
          </div>
          {searchResult && (
            <div style={{ marginBottom: 12, color: 'green' }}>
              <b>Found:</b> ID: {searchResult.id}, Lat: {searchResult.lat}, Lng: {searchResult.lng}
            </div>
          )}
          {geoLocation && (
            <div style={{ marginBottom: 12, color: 'blue' }}>
              <b>Your Location:</b> Lat: {geoLocation.lat}, Lng: {geoLocation.lng}
            </div>
          )}
          {addressLocation && (
            <div style={{ marginBottom: 12, color: 'purple' }}>
              <b>Address Location:</b> Lat: {addressLocation.lat}, Lng: {addressLocation.lng}
            </div>
          )}
          {addressError && (
            <div style={{ marginBottom: 12, color: 'red' }}>{addressError}</div>
          )}
          {/* Map moved to bottom of page */}
        </div>
      </div>
      {/* ...existing code for header and vendors section... */}
      <header>
        <div className="container">
          <div className="header-content">
            <div className="producer-brand">
              <div className="brand-logo">🏢</div>
              <h1>PRODUCER</h1>
              <p>Your Favorite Food, Delivered</p>
            </div>
            <div className="header-stats">
              <div className="stat">
                <h3>50+</h3>
                <p>Restaurants</p>
              </div>
              <div className="stat">
                <h3>10k+</h3>
                <p>Happy Customers</p>
              </div>
              <div className="stat">
                <h3>24/7</h3>
                <p>Delivery</p>
              </div>
            </div>
          </div>
        </div>
      </header>
      <section className="vendors-section">
        <div className="container">
          <h2 className="section-title">Popular Restaurants</h2>
          <div className="vendors-grid">
            {/* Only render vendor cards here, no search or map code inside vendor cards */}
            {vendorsSafe.map((vendor) => (
              <div key={vendor.id} className="vendor-card">
                <div 
                  className="vendor-header"
                  style={{
                    background: `linear-gradient(135deg, ${vendor.colors[0]}, ${vendor.colors[1]})`
                  }}
                >
                  <div className="vendor-image">
                    {vendor.image && vendor.image.startsWith('/') ? (
                      <img 
                        src={vendor.image} 
                        alt={`${vendor.name} Logo`}
                        className="vendor-logo"
                        onError={(e) => {
                          e.target.style.display = 'none';
                          e.target.nextSibling.style.display = 'block';
                        }}
                      />
                    ) : null}
                    <div 
                      className="vendor-emoji" 
                      style={{ display: vendor.image && vendor.image.startsWith('/') ? 'none' : 'block' }}
                    >
                      {vendor.fallbackImage || vendor.image}
                    </div>
                  </div>
                  <div className="vendor-badge">
                    {vendor.rating > 0 ? (
                      <span>⭐ {vendor.rating}</span>
                    ) : (
                      <span>🏪 New</span>
                    )}
                  </div>
                </div>
                <div className="vendor-content">
                  <h3>{vendor.name}</h3>
                  <p className="vendor-description">{vendor.description}</p>
                  <div className="vendor-meta">
                    <span className="cuisine-tag">{vendor.cuisine}</span>
                    {vendor.rating > 0 ? (
                      <div className="delivery-info-card">
                        <span>🕒 {vendor.deliveryTime}</span>
                        <span>🚚 {vendor.deliveryFee}</span>
                      </div>
                    ) : (
                      <div className="coming-soon-info">
                        <span>Opening Soon</span>
                      </div>
                    )}
                  </div>
                </div>
                <div className="vendor-footer">
                  {vendor.path === '#' ? (
                    <button className="vendor-btn coming-soon" disabled>
                      Coming Soon
                    </button>
                  ) : (
                    <Link to={vendor.path} className="vendor-btn">
                      Order Now
                    </Link>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
      {/* DEBUG: Map section at the bottom of the Landing Page */}
      <div style={{ width: '100%', margin: '32px 0 0 0', borderTop: '2px solid #eee', paddingTop: 16 }}>
        <h3 style={{textAlign:'center',color:'#007bff',marginBottom:8}}>Map Section (should always be visible at the bottom)</h3>
        <MapContainer center={addressLocation ? [addressLocation.lat, addressLocation.lng] : geoLocation ? [geoLocation.lat, geoLocation.lng] : searchResult ? [searchResult.lat, searchResult.lng] : [-17.8252, 31.0335]} zoom={13} style={{ height: '350px', width: '100%' }}>
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution="&copy; OpenStreetMap contributors"
          />
          {positions.map((pos) => (
            <Marker key={pos.id} position={[pos.lat, pos.lng]}>
              <Popup>
                <b>ID:</b> {pos.id}<br />
                Lat: {pos.lat}, Lng: {pos.lng}
              </Popup>
            </Marker>
          ))}
          {geoLocation && (
            <Marker position={[geoLocation.lat, geoLocation.lng]}>
              <Popup>
                <b>Your Location</b><br />
                Lat: {geoLocation.lat}, Lng: {geoLocation.lng}
              </Popup>
            </Marker>
          )}
          {addressLocation && (
            <Marker position={[addressLocation.lat, addressLocation.lng]}>
              <Popup>
                <b>Address Location</b><br />
                Lat: {addressLocation.lat}, Lng: {addressLocation.lng}
              </Popup>
            </Marker>
          )}
          {searchResult && (
            <Marker position={[searchResult.lat, searchResult.lng]}>
              <Popup>
                <b>Found by ID</b><br />
                Lat: {searchResult.lat}, Lng: {searchResult.lng}
              </Popup>
            </Marker>
          )}
        </MapContainer>
      </div>
    </div>
  );
};

export default LandingPage;
