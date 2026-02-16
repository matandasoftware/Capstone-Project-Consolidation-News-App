# News Application - Django Project

A comprehensive Django-based news application that allows readers to view articles published by publishers and independent journalists. The application features a role-based permission system, article approval workflow, email notifications, X (Twitter) integration, and RESTful API for third-party access.
---
## ⚠️ ALTERNATIVE DOWNLOAD - BACKUP ZIP FILE

**If you experience file corruption or issues cloning this repository**, a clean backup ZIP file is available:

📦 **[Download: NewsApplication_Submission_SECURE.zip](./NewsApplication_Submission_SECURE.zip)**

**What's included in the ZIP:**
- Complete source code with all module docstrings
- Sphinx documentation source files (docs/)
- Dockerfile and Docker configuration
- README.md with full setup instructions
- requirements.txt and all configuration files

**What's excluded (can be regenerated):**
- Virtual environment (venv/) - Create with: `python -m venv venv`
- Git history (.git/) - Already on GitHub
- Python cache (__pycache__/) - Auto-generated
- Built documentation (docs/_build/) - Build with: `cd docs && make html`
- IDE settings (.vs/) - Visual Studio temporary files

**To use the ZIP:**
1. Download and extract `Final-Capstone-News-App-BACKUP.zip`
2. Follow the installation instructions below
3. All functionality is preserved

---


## 📋 Table of Contents
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation & Setup](#installation--setup)
- [Database Configuration](#database-configuration)
- [Running the Application](#running-the-application)
- [User Roles & Permissions](#user-roles--permissions)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)

## ✨ Features

- **Custom User Model** with three roles: Reader, Editor, and Journalist
- **Publisher Management** with multiple editors and journalists
- **Article System** with editor approval workflow
- **Newsletter Publishing** for independent journalists
- **Role-Based Access Control** using Django groups and permissions
- **Email Notifications** to subscribers when articles are approved
- **X (Twitter) Integration** for automatic article posting
- **RESTful API** for third-party access to articles
- **Token-Based Authentication** for API access
- **Comprehensive Admin Interface** for content management

## 💻 System Requirements

- Python 3.8 or higher
- MariaDB 10.5 or higher / MySQL 8.0 or higher
- pip (Python package manager)
- Git (for cloning the repository)


## 🐳 Docker Setup (Alternative Method)

You can run this application using Docker without manually setting up Python, virtual environment, or MariaDB.

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running

### Quick Start with Docker

1. **Build the Docker image:**

​```bash
docker build -t news-app .
​```

This creates a Docker image named `news-app` with all dependencies.

2. **Run the container:**

​```bash
docker run -p 8000:8000 news-app
​```

Access the application at: http://localhost:8000

### Docker Commands Reference

**Build image:**

​```bash
docker build -t news-app .
​```

**Run container:**

​```bash
docker run -p 8000:8000 news-app
​```

**Run container in detached mode (background):**

​```bash
docker run -d -p 8000:8000 --name news-app-container news-app
​```

**Stop container:**

​```bash
docker stop news-app-container
​```

**Remove container:**

​```bash
docker rm news-app-container
​```

**View logs:**

​```bash
docker logs news-app-container
​```

**Access container shell:**

​```bash
docker exec -it news-app-container bash
​```

### What the Dockerfile Does

- **Base Image:** Uses Python 3.12 slim image
- **Dependencies:** Installs MariaDB client libraries and Python packages
- **Port:** Exposes port 8000 for Django development server
- **Auto-start:** Runs `python manage.py runserver` on container start

### Note
The Dockerfile is configured for development. For production deployment, use a production-ready web server like Gunicorn with Nginx.

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/hyperiondev-bootcamps/PC25060018465.git
cd "PC25060018465/SORTWARE ENGINEERING/Task names/News Application"
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** If you encounter issues installing `mysqlclient`, you may need to install additional system dependencies:

**Windows:**
- Download and install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

**macOS:**
```bash
brew install mysql
```

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
```

## 🗄️ Database Configuration

### Step 1: Install MariaDB

**Windows:**
- Download from [MariaDB Downloads](https://mariadb.org/download/)
- Install and note the root password you set during installation

**macOS:**
```bash
brew install mariadb
brew services start mariadb
mysql_secure_installation
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install mariadb-server
sudo mysql_secure_installation
```

### Step 2: Create Database and User

Open MariaDB/MySQL shell:
```bash
mysql -u root -p
```

Run the following SQL commands:
```sql
CREATE DATABASE news_app_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'news_app_user'@'localhost' IDENTIFIED BY 'news_app_password';
GRANT ALL PRIVILEGES ON news_app_db.* TO 'news_app_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 3: Update Database Credentials (Optional)

If you want to use different database credentials, edit `news_project/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',        # Default: news_app_db
        'USER': 'your_database_user',        # Default: news_app_user
        'PASSWORD': 'your_password',         # Default: news_app_password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Step 4: Apply Migrations

With your virtual environment activated and database configured:

```bash
python manage.py makemigrations
python manage.py migrate
```

**Expected Output:**
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  ...
  Applying news_app.0001_initial... OK
```

### Step 5: Set Up User Groups and Permissions

Run the custom management command to create groups and assign permissions:

```bash
python manage.py setup_groups
```

**Expected Output:**
```
Successfully created/updated groups:
  - readers_group
  - editors_group
  - journalists_group
All permissions have been assigned successfully!
```

### Step 6: Create Superuser

Create an admin account to access the Django admin interface:

```bash
python manage.py createsuperuser
```

Follow the prompts to set:
- Username
- Email address
- Password (enter twice)

## 🏃 Running the Application

### Start Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

### Access Admin Interface

Navigate to: **http://127.0.0.1:8000/admin/**

Login with the superuser credentials you created.

## 👥 User Roles & Permissions

### Reader
- **Permissions:** Can only view articles and newsletters
- **Custom Fields:**
  - Subscriptions to publishers
  - Subscriptions to journalists
- **Group:** `readers_group`

### Editor
- **Permissions:** Can view, update, and delete articles and newsletters
- **Special Permission:** Can approve articles for publishing
- **Group:** `editors_group`

### Journalist
- **Permissions:** Can create, view, update, and delete articles and newsletters
- **Custom Fields:**
  - Independent articles
  - Independent newsletters
- **Group:** `journalists_group`

## 🔌 API Documentation

### Base URL
```
http://127.0.0.1:8000/api/
```

### Endpoints

#### 1. Get Auth Token
```http
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**
```json
{
    "token": "abc123def456..."
}
```

#### 2. List Subscribed Articles (Authenticated)
```http
GET /api/articles/subscribed/
Authorization: Token abc123def456...
```

**Response:**
```json
[
    {
        "id": 1,
        "title": "Article Title",
        "slug": "article-title",
        "summary": "Brief summary...",
        "content": "Full article content...",
        "author": {
            "id": 2,
            "username": "journalist1",
            "role": "JOURNALIST"
        },
        "publisher": {
            "id": 1,
            "name": "The Daily News"
        },
        "is_approved": true,
        "created_at": "2024-02-06T10:30:00Z"
    }
]
```

#### 3. List All Articles (Public)
```http
GET /api/articles/
```

#### 4. Get Article Detail
```http
GET /api/articles/{id}/
```

#### 5. List Publishers
```http
GET /api/publishers/
Authorization: Token abc123def456...
```

#### 6. List Journalists
```http
GET /api/journalists/
Authorization: Token abc123def456...
```

### Testing the API

**Using cURL:**
```bash
# Get token
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "reader1", "password": "password123"}'

# Get subscribed articles
curl http://127.0.0.1:8000/api/articles/subscribed/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Using Python requests:**
```python
import requests

# Get token
response = requests.post('http://127.0.0.1:8000/api/token/', 
    json={'username': 'reader1', 'password': 'password123'})
token = response.json()['token']

# Get subscribed articles
headers = {'Authorization': f'Token {token}'}
articles = requests.get('http://127.0.0.1:8000/api/articles/subscribed/', 
    headers=headers)
print(articles.json())
```

## 🧪 Testing

### Run All Tests

```bash
python manage.py test
```

### Run Specific Test Module

```bash
python manage.py test news_app.tests.ModelTests
```

### Run Tests with Coverage (Optional)

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Scenarios Covered

- ✅ CustomUser model creation and role assignment
- ✅ Group auto-assignment based on user role
- ✅ Publisher with editors and journalists
- ✅ Article creation and approval workflow
- ✅ Newsletter creation
- ✅ API authentication and authorization
- ✅ API returns correct articles based on subscriptions
- ✅ Permission checks for different user roles

## 📁 Project Structure

```
News Application/
├── news_project/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py              # Main configuration (Database, Apps, etc.)
│   ├── urls.py                  # Project-level URL routing
│   ├── wsgi.py
│   └── asgi.py
├── news_app/                     # Main application
│   ├── migrations/              # Database migrations
│   ├── management/              # Custom management commands
│   │   └── commands/
│   │       └── setup_groups.py  # Creates groups and assigns permissions
│   ├── templates/               # HTML templates
│   │   └── news_app/
│   │       ├── article_list.html
│   │       ├── article_detail.html
│   │       └── approve_articles.html
│   ├── __init__.py
│   ├── admin.py                 # Admin interface configuration
│   ├── api_views.py             # RESTful API views
│   ├── apps.py                  # App configuration (loads signals)
│   ├── forms.py                 # Django forms
│   ├── models.py                # Database models (CustomUser, Publisher, etc.)
│   ├── serializers.py           # DRF serializers for API
│   ├── signals.py               # Email & X (Twitter) integration
│   ├── tests.py                 # Automated unit tests
│   ├── twitter_utils.py         # X API helper functions
│   ├── urls.py                  # App-level URL routing
│   └── views.py                 # View functions
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── .gitignore                   # Git ignore file
└── Documentation/               # Additional documentation
    ├── COMPLETE_OVERVIEW.md
    ├── DESIGN_DOCUMENT.md
    ├── EXPLANATION_models.md
    ├── EXPLANATION_admin.md
    ├── EXPLANATION_signals.md
    └── QUICK_REFERENCE.md
```

## 🎯 Usage Examples

### Creating Test Data via Admin

1. **Access Admin:** http://127.0.0.1:8000/admin/
2. **Create a Publisher:**
   - Click "Publishers" → "Add Publisher"
   - Enter name, description, website
   - Save
3. **Create a Journalist:**
   - Click "Users" → "Add User"
   - Set username and password
   - In user details, set role to "Journalist"
   - Save
4. **Create an Editor:**
   - Same as journalist but set role to "Editor"
5. **Create a Reader:**
   - Same as above but set role to "Reader"
   - In subscriptions section, add publisher/journalist subscriptions
6. **Create an Article:**
   - Click "Articles" → "Add Article"
   - Enter title, content, summary
   - Select journalist as author
   - Optionally select publisher
   - Leave "is_approved" unchecked initially
   - Save

### Testing Article Approval Workflow

1. **As Editor:** Login to admin interface
2. **Navigate to Articles**
3. **Select an article** and check the "is_approved" checkbox
4. **Save the article**
5. **Check console output** for:
   - Email notification confirmation
   - X (Twitter) posting confirmation (if configured)

### Testing Email Notifications

When an article is approved, the console will display:
```
Email sent to reader@example.com for article: Article Title
Subject: New Article Published: Article Title
```

### Configuring X (Twitter) Integration

Edit `news_project/settings.py`:
```python
TWITTER_API_KEY = 'your_api_key'
TWITTER_API_SECRET = 'your_api_secret'
TWITTER_ACCESS_TOKEN = 'your_access_token'
TWITTER_ACCESS_TOKEN_SECRET = 'your_access_token_secret'
TWITTER_ENABLED = True
```

## 🐛 Troubleshooting

### Issue: Cannot connect to database
**Solution:** Verify MariaDB is running and credentials are correct
```bash
# Check if MariaDB is running
sudo systemctl status mariadb

# Test connection
mysql -u news_app_user -p news_app_db
```

### Issue: mysqlclient installation fails
**Solution:** Install system dependencies first (see Installation section above)

### Issue: Migrations not applied
**Solution:** Run migrations explicitly
```bash
python manage.py migrate
```

### Issue: Permission denied errors
**Solution:** Run setup_groups command
```bash
python manage.py setup_groups
```

### Issue: API returns 401 Unauthorized
**Solution:** Ensure you're including the Authorization header with valid token
```bash
Authorization: Token YOUR_TOKEN_HERE
```

## 📞 Support

For questions or issues, please refer to the documentation files in the project or contact the development team.

## 📝 License

This project is part of an academic submission for HyperionDev.

## 🙏 Acknowledgments

- Django Framework
- Django REST Framework
- X (Twitter) API
- MariaDB/MySQL Database


