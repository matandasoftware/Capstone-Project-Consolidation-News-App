import React, { useEffect, useRef, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import io from 'socket.io-client';

// Fix default marker icon issue in Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const SOCKET_SERVER_URL = 'http://localhost:5000'; // Update if your backend runs elsewhere


const Admin = () => {
  const [positions, setPositions] = useState([]); // [{id, lat, lng}]
  const [tracking, setTracking] = useState(false);
  const [searchId, setSearchId] = useState('');
  const [searchResult, setSearchResult] = useState(null);
  const socketRef = useRef(null);

  useEffect(() => {
    if (!tracking) return;
    // Connect to socket.io server
    socketRef.current = io(SOCKET_SERVER_URL);

    // Listen for location updates
    socketRef.current.on('locationUpdate', (data) => {
      setPositions((prev) => {
        // Update or add marker by id
        const idx = prev.findIndex((p) => p.id === data.id);
        if (idx !== -1) {
          const updated = [...prev];
          updated[idx] = data;
          return updated;
        }
        return [...prev, data];
      });
    });

    return () => {
      socketRef.current.disconnect();
    };
  }, [tracking]);

  const handleTrackingToggle = () => {
    setTracking((prev) => !prev);
    if (!tracking) setPositions([]); // Clear positions when starting
  };

  const handleSearch = () => {
    if (!searchId) {
      setSearchResult(null);
      return;
    }
    const found = positions.find((pos) => String(pos.id) === searchId);
    setSearchResult(found || null);
  };

  return (
    <div className="page admin-page">
      <div className="container">
        <h1>Admin Dashboard</h1>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center', marginBottom: 16 }}>
          <button onClick={handleTrackingToggle}>
            {tracking ? 'Stop Real-time Tracking' : 'Start Real-time Tracking'}
          </button>
          <input
            type="text"
            placeholder="Search by ID..."
            value={searchId}
            onChange={e => setSearchId(e.target.value)}
            style={{ padding: '4px 8px' }}
          />
          <button onClick={handleSearch}>Search</button>
        </div>
        {searchResult && (
          <div style={{ marginBottom: 12, color: 'green' }}>
            <b>Found:</b> ID: {searchResult.id}, Lat: {searchResult.lat}, Lng: {searchResult.lng}
          </div>
        )}
        <p>Real-time tracking map below:</p>
        <div style={{ height: '500px', width: '100%', marginBottom: 20 }}>
          <MapContainer center={[-17.8252, 31.0335]} zoom={13} style={{ height: '100%', width: '100%' }}>
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
          </MapContainer>
        </div>
      </div>
    </div>
  );
};

export default Admin;
