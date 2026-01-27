# Buroko's Kitchen - GitHub Upload Instructions

## Prerequisites
1. Install Git: https://git-scm.com/download/windows
2. Create a GitHub account: https://github.com
3. Create a new repository on GitHub named "buroko-kitchen"

## Upload Commands (Run in terminal after installing Git)

# Navigate to project directory
cd "C:\Users\pfare\Documents\ACADEMICS\SORTWARE ENGINEERING\New workspace for app"

# Initialize Git repository
git init

# Add all files to staging
git add .

# Create initial commit
git commit -m "Initial commit: Buroko's Kitchen food ordering application"

# Add GitHub repository as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin <https://github.com/YOUR_USERNAME/buroko-kitchen.git>

# Create main branch and push to GitHub
git branch -M main
git push -u origin main

## Alternative: Using GitHub Desktop
1. Download GitHub Desktop: https://desktop.github.com/
2. Install and sign in to your GitHub account
3. Click "Add an Existing Repository from your Hard Drive"
4. Select the project folder
5. Publish to GitHub

## Alternative: Using GitHub Web Interface
1. Create a new repository on GitHub
2. Use "uploading an existing file" option
3. Drag and drop all project files (except node_modules)
4. Commit changes

## Project Features
- ✅ React 18 frontend with responsive design
- ✅ Node.js/Express backend API
- ✅ MongoDB database integration
- ✅ Firebase authentication
- ✅ WhatsApp ordering integration
- ✅ Capitec EFT payment system
- ✅ Original Buroko's Kitchen menu items
- ✅ Shopping cart and order management
- ✅ Admin dashboard functionality

## Important Notes
- node_modules folders are already excluded via .gitignore
- Environment variables (.env files) are excluded for security
- All sensitive data should be added to environment variables
