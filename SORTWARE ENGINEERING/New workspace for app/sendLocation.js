const axios = require('axios');

const SERVER_URL = 'http://localhost:5000/api/track'; // Update if your backend runs elsewhere
const id = 'device-123'; // Unique identifier for the tracked entity

// Example: Simulate movement
let lat = -17.8252;
let lng = 31.0335;

setInterval(async () => {
  // Simulate small random movement
  lat += (Math.random() - 0.5) * 0.001;
  lng += (Math.random() - 0.5) * 0.001;

  try {
    const res = await axios.post(SERVER_URL, { id, lat, lng });
    console.log(`Sent: ${lat}, ${lng} | Response:`, res.data);
  } catch (err) {
    console.error('Error sending location:', err.response ? err.response.data : err.message);
  }
}, 2000); // Send every 2 seconds
