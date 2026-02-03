# 🚀 TASK 2 DEPLOYMENT COMMANDS

Execute these commands in order to deploy your CV webpage.

---

## 📋 **PREREQUISITES:**

✅ You already have:
- CV files ready in Task2-MyCV folder
- GitHub account (matandasoftware)
- Git configured locally

---

## 🎯 **STEP 1: CREATE GITHUB REPOSITORY (WEB)**

**Do this manually on GitHub.com:**

1. Go to: https://github.com/new
2. Repository name: **MyCV** (exactly this)
3. Description: "Professional CV Webpage - Pfarelo Channel Mudau"
4. Select: **PUBLIC** ✅
5. DO NOT check "Add README"
6. Click: **"Create repository"**

---

## 🚀 **STEP 2: DEPLOY CV TO GITHUB (COMMANDS)**

### **Option A: If you want to push from Task2-MyCV folder**

```powershell
# Navigate to Task2-MyCV folder
cd "C:\Users\pfare\OneDrive\Documentos\ACADEMICS\SORTWARE ENGINEERING\Task names\Deployment of static website\Task2-MyCV"

# Initialize git repository
git init

# Add only the CV files (not README or other docs)
git add index.html styles.css

# Commit
git commit -m "Initial CV webpage deployment"

# Set main branch
git branch -M main

# Add remote
git remote add origin https://github.com/matandasoftware/MyCV.git

# Push to GitHub
git push -u origin main
```

### **Option B: If you want cleaner approach (create fresh folder)**

```powershell
# Create temporary deployment folder
New-Item -Path "C:\Users\pfare\Desktop\MyCV-Deploy" -ItemType Directory -Force

# Copy only deployment files
Copy-Item -Path "C:\Users\pfare\OneDrive\Documentos\ACADEMICS\SORTWARE ENGINEERING\Task names\Deployment of static website\Task2-MyCV\index.html" -Destination "C:\Users\pfare\Desktop\MyCV-Deploy\"
Copy-Item -Path "C:\Users\pfare\OneDrive\Documentos\ACADEMICS\SORTWARE ENGINEERING\Task names\Deployment of static website\Task2-MyCV\styles.css" -Destination "C:\Users\pfare\Desktop\MyCV-Deploy\"

# Navigate to deployment folder
cd "C:\Users\pfare\Desktop\MyCV-Deploy"

# Initialize and push
git init
git add .
git commit -m "Deploy professional CV webpage"
git branch -M main
git remote add origin https://github.com/matandasoftware/MyCV.git
git push -u origin main
```

---

## 🌐 **STEP 3: ENABLE GITHUB PAGES**

### **Manual Steps (do on GitHub.com):**

1. Go to: https://github.com/matandasoftware/MyCV
2. Click: **Settings** tab
3. Click: **Pages** (left sidebar)
4. Under **"Source"**:
   - Branch: Select **main**
   - Folder: Select **/ (root)**
5. Click: **Save**
6. Wait 2-3 minutes
7. Refresh page
8. You'll see: **"Your site is live at https://matandasoftware.github.io/MyCV/"**

---

## 📸 **STEP 4: TAKE SCREENSHOT**

1. Go to: https://matandasoftware.github.io/MyCV/
2. Wait for page to load completely
3. Press: **Windows Key + Shift + S**
4. Select: **Entire page including URL bar**
5. Open: **Paint** (press Windows Key, type "paint")
6. Press: **Ctrl + V** (paste)
7. Save as: `my_cv.png`
8. Save to: `C:\Users\pfare\OneDrive\Documentos\ACADEMICS\SORTWARE ENGINEERING\Task names\Deployment of static website\Task2-MyCV\`

---

## 📝 **STEP 5: UPDATE my_cv.txt**

### **Command to update file:**

```powershell
# Update my_cv.txt with your actual URL
Set-Content -Path "C:\Users\pfare\OneDrive\Documentos\ACADEMICS\SORTWARE ENGINEERING\Task names\Deployment of static website\Task2-MyCV\my_cv.txt" -Value "https://matandasoftware.github.io/MyCV/"
```

**Or manually:**
1. Open: `Task2-MyCV\my_cv.txt`
2. Replace content with: `https://matandasoftware.github.io/MyCV/`
3. Save file

---

## 🎯 **STEP 6: PUSH TO HYPERIONDEV REPO**

### **Commands:**

```powershell
# Navigate to HyperionDev repo
cd "C:\Users\pfare\source\repos\hyperiondev-bootcamps\PC25060018465"

# Create Task2-MyCV folder
New-Item -Path "Level 3 - Deployment and Development Workflows\M07T01 – Deployment of Static Websites\Task2-MyCV" -ItemType Directory -Force

# Copy CV files (excluding README and CODE_REVIEW)
Copy-Item -Path "C:\Users\pfare\OneDrive\Documentos\ACADEMICS\SORTWARE ENGINEERING\Task names\Deployment of static website\Task2-MyCV\index.html" -Destination "Level 3 - Deployment and Development Workflows\M07T01 – Deployment of Static Websites\Task2-MyCV\" -Force

Copy-Item -Path "C:\Users\pfare\OneDrive\Documentos\ACADEMICS\SORTWARE ENGINEERING\Task names\Deployment of static website\Task2-MyCV\styles.css" -Destination "Level 3 - Deployment and Development Workflows\M07T01 – Deployment of Static Websites\Task2-MyCV\" -Force

Copy-Item -Path "C:\Users\pfare\OneDrive\Documentos\ACADEMICS\SORTWARE ENGINEERING\Task names\Deployment of static website\Task2-MyCV\my_cv.txt" -Destination "Level 3 - Deployment and Development Workflows\M07T01 – Deployment of Static Websites\Task2-MyCV\" -Force

Copy-Item -Path "C:\Users\pfare\OneDrive\Documentos\ACADEMICS\SORTWARE ENGINEERING\Task names\Deployment of static website\Task2-MyCV\my_cv.png" -Destination "Level 3 - Deployment and Development Workflows\M07T01 – Deployment of Static Websites\Task2-MyCV\" -Force

# Add to git
git add "Level 3 - Deployment and Development Workflows/M07T01 – Deployment of Static Websites/Task2-MyCV/"

# Check status
git status

# Commit
git commit -m "Add Task 2: Professional CV Webpage Deployment"

# Push
git push origin main
```

---

## ✅ **STEP 7: VERIFY EVERYTHING**

### **Checklist:**

```powershell
# Check Task2-MyCV folder in HyperionDev repo
Get-ChildItem -Path "C:\Users\pfare\source\repos\hyperiondev-bootcamps\PC25060018465\Level 3 - Deployment and Development Workflows\M07T01 – Deployment of Static Websites\Task2-MyCV"
```

**Should show:**
- index.html
- styles.css
- my_cv.txt
- my_cv.png

### **Test URLs:**

1. **GitHub Repository:** https://github.com/matandasoftware/MyCV
2. **Live CV Website:** https://matandasoftware.github.io/MyCV/
3. **HyperionDev Repo:** https://github.com/hyperiondev-bootcamps/PC25060018465

---

## 📊 **SUMMARY OF WHAT YOU'LL HAVE:**

### **On GitHub (matandasoftware/MyCV):**
- index.html
- styles.css

### **On GitHub Pages:**
- Live website at: https://matandasoftware.github.io/MyCV/

### **In HyperionDev Repo:**
```
Level 3 - Deployment and Development Workflows/
└── M07T01 – Deployment of Static Websites/
    ├── Task1-HealthyCooking/
    │   ├── index.html
    │   ├── Styles.css
    │   ├── static_url.txt
    │   ├── static_page.png
    │   └── pictures/
    └── Task2-MyCV/
        ├── index.html
        ├── styles.css
        ├── my_cv.txt
        └── my_cv.png
```

---

## 🚨 **TROUBLESHOOTING:**

### **If "remote already exists" error:**
```powershell
git remote remove origin
git remote add origin https://github.com/matandasoftware/MyCV.git
```

### **If "repository not found" error:**
Make sure you created the MyCV repository on GitHub first!

### **If GitHub Pages shows 404:**
- Wait 3-5 minutes
- Check Settings → Pages is enabled
- Verify branch is set to "main"
- Clear browser cache (Ctrl + Shift + R)

### **If screenshot is too large:**
```powershell
# Resize using PowerShell (requires .NET)
Add-Type -AssemblyName System.Drawing
$img = [System.Drawing.Image]::FromFile("C:\path\to\my_cv.png")
$newWidth = 1920
$newHeight = ($img.Height / $img.Width) * $newWidth
$thumb = New-Object System.Drawing.Bitmap($newWidth, $newHeight)
$graphics = [System.Drawing.Graphics]::FromImage($thumb)
$graphics.DrawImage($img, 0, 0, $newWidth, $newHeight)
$thumb.Save("C:\path\to\my_cv_resized.png")
$img.Dispose()
$thumb.Dispose()
```

---

## 🎉 **WHEN COMPLETE:**

You'll have:
- ✅ Live CV at GitHub Pages
- ✅ Screenshot with URL
- ✅ URL saved in txt file
- ✅ Everything pushed to HyperionDev repo
- ✅ Task 2 COMPLETE!

---

## 📞 **NEED HELP?**

Just tell me:
1. Which step you're on
2. What command you ran
3. What error/output you got

I'll help you fix it! 🚀

---

**Ready to execute?** Start with Step 1 (create GitHub repo) and work your way down! 💪