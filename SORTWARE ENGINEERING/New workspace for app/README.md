# Buroko's Kitchen - Food Ordering Application

A modern, full-stack food ordering application built for Buroko's Kitchen restaurant in Thohoyandou, South Africa.

## 🚀 Features

### Customer Features
- **Browse Menu** - View categorized food items with descriptions and prices
- **Search & Filter** - Find items by name, description, or category
- **Shopping Cart** - Add/remove items, adjust quantities
- **User Authentication** - Firebase-powered registration and login
- **Order Placement** - Complete checkout with customer details
- **Order Tracking** - Real-time order status updates
- **Order History** - View past orders and reorder favorites
- **Responsive Design** - Works seamlessly on desktop and mobile

### Admin Features
- **Order Management** - View, update, and track all orders
- **Menu Management** - Add, edit, and manage menu items
- **Dashboard** - Overview of daily orders and sales
- **Customer Management** - View customer information and order history

## 🛠 Tech Stack

### Frontend
- **React 18** - Modern React with hooks and functional components
- **React Router DOM** - Client-side routing
- **Context API** - State management for cart, auth, and notifications
- **Firebase Auth** - User authentication and authorization
- **Axios** - HTTP client for API communication
- **Lucide React** - Beautiful icons
- **React Toastify** - Toast notifications
- **CSS3** - Modern styling with Flexbox and Grid

### Backend
- **Node.js** - JavaScript runtime
- **Express.js** - Web application framework
- **MongoDB** - NoSQL database with Mongoose ODM
- **Firebase Admin** - Server-side Firebase integration
- **Multer** - File upload handling
- **Express Validator** - Input validation and sanitization
- **Helmet** - Security middleware
- **Morgan** - HTTP request logging
- **CORS** - Cross-origin resource sharing

## 📁 Project Structure

```
buroko-kitchen/
├── client/                 # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── context/        # React Context providers
│   │   ├── pages/          # Route components
│   │   ├── config/         # Configuration files
│   │   ├── styles/         # CSS stylesheets
│   │   ├── App.js          # Main App component
│   │   └── index.js        # Entry point
│   └── package.json
├── server/                 # Express backend
│   ├── config/             # Database and other configs
│   ├── models/             # Mongoose schemas
│   ├── routes/             # API routes
│   ├── uploads/            # File upload directory
│   ├── index.js            # Server entry point
│   └── package.json
├── .github/
│   └── copilot-instructions.md
└── README.md
```

## 🔧 Installation & Setup

### Prerequisites
- Node.js (v14 or higher)
- MongoDB (local or cloud)
- Firebase project (for authentication)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd buroko-kitchen
```

### 2. Install Dependencies
```bash
# Install root dependencies
npm install

# Install client dependencies
cd client
npm install

# Install server dependencies
cd ../server
npm install
```

### 3. Environment Configuration

#### Server Environment (.env in server folder)
```env
# Database
MONGODB_URI=mongodb://localhost:27017/buroko-kitchen

# Server Configuration
PORT=5000
NODE_ENV=development
CLIENT_URL=http://localhost:3000

# Firebase Admin (get from Firebase Console)
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-...@your-project.iam.gserviceaccount.com
```

#### Client Firebase Configuration
Update `client/src/config/firebase.js` with your Firebase project settings:
```javascript
const firebaseConfig = {
  apiKey: "your-api-key",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "your-app-id"
};
```

### 4. Database Setup

#### MongoDB Setup
1. Install MongoDB locally or use MongoDB Atlas
2. Create a database named `buroko-kitchen`
3. Update the `MONGODB_URI` in your server `.env` file

#### Sample Data (Optional)
You can seed the database with sample menu items using the MongoDB shell or a database client.

### 5. Firebase Setup
1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com)
2. Enable Authentication with Email/Password
3. Create a Firestore database
4. Generate Firebase Admin SDK credentials
5. Update configuration files with your Firebase credentials

## 🚀 Running the Application

### Development Mode
```bash
# From project root - runs both client and server
npm run dev

# Or run separately:
# Terminal 1 - Server
cd server
npm run dev

# Terminal 2 - Client
cd client
npm start
```

### Production Build
```bash
# Build client for production
cd client
npm run build

# Start server in production mode
cd ../server
NODE_ENV=production npm start
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

## 📱 Usage

### For Customers
1. **Browse Menu**: Visit the menu page to see available items
2. **Add to Cart**: Click "Add to Cart" for desired items
3. **Register/Login**: Create an account or sign in
4. **Checkout**: Provide delivery details and place order
5. **Track Order**: Monitor order status in real-time

### For Admins
1. **Login**: Use admin credentials (admin@buroko.com)
2. **Manage Orders**: View and update order statuses
3. **Menu Management**: Add, edit, or remove menu items
4. **Dashboard**: Monitor daily sales and performance

## 🔌 API Endpoints

### Orders
- `GET /api/orders` - Get all orders (admin)
- `POST /api/orders` - Create new order
- `GET /api/orders/:id` - Get specific order
- `PUT /api/orders/:id/status` - Update order status
- `GET /api/orders/customer/:email` - Get customer orders
- `DELETE /api/orders/:id` - Cancel order

### Menu
- `GET /api/menu` - Get all menu items
- `POST /api/menu` - Add new menu item (admin)
- `PUT /api/menu/:id` - Update menu item (admin)
- `DELETE /api/menu/:id` - Delete menu item (admin)

### Upload
- `POST /api/upload` - Upload images for menu items

## 🎨 Customization

### Styling
- Primary styles are in `client/src/styles/global.css`
- Component-specific styles can be added as CSS modules
- Color scheme can be customized by updating CSS custom properties

### Adding Features
1. **New Pages**: Add components in `client/src/pages/`
2. **New API Routes**: Add routes in `server/routes/`
3. **Database Models**: Add schemas in `server/models/`

## 🔒 Security Features

- **Input Validation**: Server-side validation using express-validator
- **Authentication**: Firebase Authentication with JWT tokens
- **Authorization**: Protected routes for admin functions
- **Security Headers**: Helmet.js for security headers
- **CORS Configuration**: Restricted cross-origin requests
- **File Upload Security**: Restricted file types and sizes

## 📱 Mobile Responsiveness

The application is fully responsive and optimized for:
- Desktop computers (1200px+)
- Tablets (768px - 1199px)
- Mobile phones (320px - 767px)

## 🚀 Deployment

### Frontend (Vercel/Netlify)
1. Build the client: `cd client && npm run build`
2. Deploy the `build` folder to your hosting service
3. Configure environment variables

### Backend (Heroku/Railway/DigitalOcean)
1. Ensure all environment variables are set
2. Deploy the `server` folder
3. Configure MongoDB connection string

### Environment Variables for Production
- Set `NODE_ENV=production`
- Update `CLIENT_URL` to your frontend domain
- Use production MongoDB URI
- Configure Firebase credentials securely

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support or questions:
- **Restaurant**: Buroko's Kitchen, Thohoyandou
- **Developer**: Contact through GitHub issues

## 🏪 Business Information

- **Restaurant**: Buroko's Kitchen
- **Location**: Thohoyandou, South Africa
- **Delivery Fee**: R14.00
- **Hours**: 
  - Monday - Friday: 09:00 - 18:00
  - Saturday: 09:00 - 16:00
  - Sunday: Closed

---

*Built with ❤️ for Buroko's Kitchen*
