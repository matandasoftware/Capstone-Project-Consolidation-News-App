# Deployment Guide for Buroko's Kitchen

## Local Development Setup (After GitHub Clone)

### Prerequisites
- Node.js (v16 or higher)
- MongoDB (local or cloud)
- Firebase account

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/buroko-kitchen.git
   cd buroko-kitchen
   ```

2. **Install dependencies**
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

3. **Environment Configuration**
   Create `.env` files in both client and server directories:
   
   **client/.env**
   ```
   REACT_APP_API_URL=http://localhost:5000
   REACT_APP_FIREBASE_API_KEY=your_firebase_api_key
   REACT_APP_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
   REACT_APP_FIREBASE_PROJECT_ID=your_project_id
   ```
   
   **server/.env**
   ```
   NODE_ENV=development
   PORT=5000
   MONGODB_URI=mongodb://localhost:27017/buroko-kitchen
   FIREBASE_SERVICE_ACCOUNT_KEY=path_to_your_service_account.json
   ```

4. **Start the application**
   ```bash
   # From root directory
   npm run dev
   ```

## Production Deployment

### Heroku Deployment
1. Install Heroku CLI
2. Create Heroku app: `heroku create buroko-kitchen`
3. Set environment variables in Heroku dashboard
4. Deploy: `git push heroku main`

### Vercel Deployment (Frontend)
1. Install Vercel CLI: `npm i -g vercel`
2. Deploy frontend: `cd client && vercel`
3. Set environment variables in Vercel dashboard

### MongoDB Atlas (Database)
1. Create account at https://cloud.mongodb.com
2. Create cluster and get connection string
3. Update MONGODB_URI in environment variables

## Firebase Setup
1. Create Firebase project
2. Enable Authentication
3. Generate service account key
4. Update Firebase configuration

## Features Included
- ✅ Responsive menu with original Buroko's Kitchen items
- ✅ Shopping cart functionality
- ✅ User authentication (Firebase)
- ✅ WhatsApp ordering integration
- ✅ Capitec EFT payment system
- ✅ Admin dashboard
- ✅ Order management system
- ✅ Mobile-optimized design

## Support
For issues or questions, create an issue in the GitHub repository.
