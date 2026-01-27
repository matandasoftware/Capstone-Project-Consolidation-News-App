# Buroko's Kitchen - Quick Start Guide

## 🚨 Current Issue: Node.js Required

The app won't start because **Node.js is not installed**. Here's how to fix it:

### ✅ **Solution Steps:**

#### 1. **Install Node.js** (Currently in progress via winget)
- Installation should complete soon
- **OR** Download manually from: https://nodejs.org/

#### 2. **Restart VS Code**
- Close VS Code completely
- Reopen to refresh environment variables

#### 3. **Verify Installation**
```powershell
node --version
npm --version
```

#### 4. **Run Setup Script**
Double-click `setup.bat` or run:
```powershell
.\setup.bat
```

#### 5. **Start the App**
```powershell
npm run dev
```

### 🔧 **If Node.js Still Not Found After Installation:**

1. **Restart Computer** (ensures PATH is updated)
2. **Manual PATH Setup:**
   - Go to System Properties > Environment Variables
   - Add `C:\Program Files\nodejs\` to PATH
   - Restart VS Code

### 📱 **What the App Will Do When Working:**

- **Frontend**: http://localhost:3000 (React app)
- **Backend**: http://localhost:5000 (Express API)
- **Features**: Menu browsing, cart, orders, admin dashboard

### 🔥 **Firebase Setup Required:**
Update `client/src/config/firebase.js` with your Firebase project config from:
https://console.firebase.google.com

### 💾 **MongoDB Setup Required:**
- Local: Install MongoDB Community Server
- Cloud: Use MongoDB Atlas (free tier)

---

**Status**: ⏳ Waiting for Node.js installation to complete...

Once Node.js is installed, the app will run perfectly! 🚀
