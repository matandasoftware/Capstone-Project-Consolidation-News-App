# eCommerce Web Application

Django-based multi-vendor eCommerce platform with role-based access control, REST API, and social media integration.

## Project Overview

This is a capstone project implementing a full-featured eCommerce system where users can register as either Vendors (sellers) or Buyers (customers).

**Key Features:**
- User authentication with vendor/buyer roles
- Multi-vendor store management
- Product catalog with stock management
- Session-based shopping cart
- Order processing with email invoices
- Verified/unverified review system
- Password reset with expiring tokens
- **RESTful API for third-party integration**
- **Automated Twitter posting for stores and products**
- MariaDB database backend
- Responsive Bootstrap 5 UI

---

## Technology Stack

**Backend:**
- Python 3.12
- Django 6.0
- Django REST Framework 3.15
- MariaDB 10.6

**Frontend:**
- HTML5/CSS3
- Bootstrap 5
- Django Templates

**APIs & Integration:**
- Twitter API v2 (automated tweeting)
- OAuth 1.0a authentication
- REST API with BasicAuth

**Key Libraries:**
- mysqlclient (database)
- Pillow (image handling)
- tweepy (Twitter integration)
- python-dotenv (environment variables)
- djangorestframework (REST API)

---

## Project Structure

```
eCommerce/
├── accounts/              # Authentication app
│   ├── models.py         # ResetToken model
│   ├── views.py          # Login, register, password reset
│   ├── forms.py          # Registration, login forms
│   └── tests.py          # Authentication tests
├── product/              # Main eCommerce app
│   ├── models.py         # Store, Product, Order, Review (with tweet_id fields)
│   ├── views.py          # All business logic
│   ├── forms.py          # Product, store, review forms
│   ├── admin.py          # Django admin config
│   ├── tests.py          # Product tests
│   ├── serializers.py    # DRF serializers for API
│   ├── api_views.py      # REST API endpoints
│   ├── api_urls.py       # API URL routing
│   ├── signals.py        # Auto-tweet signals
│   ├── twitter_utils.py  # Twitter API integration
│   ├── templates/        # HTML templates
│   └── templatetags/     # Custom template tags
├── eCommerce/            # Project settings
│   ├── settings.py       # Django configuration (with Twitter settings)
│   ├── urls.py           # Root URL config (includes API routes)
│   └── tests/            # Automated test suite
│       ├── test_authentication.py
│       ├── test_store_management.py
│       ├── test_product_management.py
│       ├── test_cart_checkout.py
│       ├── test_review_system.py
│       └── test_security_permissions.py
├── Sequence diagrams/    # API sequence diagrams (8 PDFs)
│   ├── sequence_diagram_overview.drawio.pdf
│   ├── sequence_diagram_Vendor_Creates_Store(Authenticated).drawio.pdf
│   ├── sequence_diagram_Vendor_Adds_Product_to_Store(Authenticated).drawio.pdf
│   ├── sequence_diagram_User_Views_Stores_by_Vendor(Public).drawio.pdf
│   ├── sequence_diagram_User_Views_Products_by_Store(Public).drawio.pdf
│   ├── sequence_diagram_Vendor_Retrieves_Reviews_for_Product(Public).drawio.pdf
│   ├── sequence_diagram_Complete_Purchase → Review Flow.drawio.pdf
│   └── sequence_diagram_Security_Flow - Unauthorized_Access_Attempt.drawio.pdf
├── Planning/             # Documentation
│   ├── 1_requirements.md
│   ├── 2_ui_layout.md
│   ├── 3_access_control.md
│   ├── 4_failure_handling.md
│   ├── 5_database_schema.md
│   ├── 6_test_cases.md
│   └── tests/            # Manual test documentation
├── .env                  # Twitter API credentials (not in Git)
├── .gitignore            # Git ignore file (protects .env)
├── emails/               # Email storage (development)
├── media/                # Uploaded product images
├── static/               # CSS, JS, images
├── requirements.txt      # Python dependencies
└── manage.py             # Django management script
```

---

## Setup Instructions

### 1. Prerequisites

- Python 3.12+
- MariaDB 10.6+
- pip (Python package manager)
- Twitter Developer Account (for Twitter integration)

### 2. Database Setup

**Start MariaDB:**

```sh
# Windows
net start mariadb

# Linux/Mac
sudo systemctl start mariadb
```

**Create database:**

```sh
mysql -u root -p

CREATE DATABASE ecommerce_db;
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'ecommerce_password';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Virtual Environment

**Create and activate:**

```sh
# Windows
cd eCommerce
python -m venv myenv
myenv\Scripts\activate

# Linux/Mac
cd eCommerce
python3 -m venv myenv
source myenv/bin/activate
```

### 4. Install Dependencies

```sh
pip install -r requirements.txt
```

**Or install manually:**

```sh
pip install django
pip install mysqlclient
pip install Pillow
pip install djangorestframework
pip install tweepy
pip install python-dotenv
```

### 5. Twitter API Setup

**Get Twitter API Credentials:**
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create a new app with **Read and Write** permissions
3. Generate API Keys and Access Tokens

**Create `.env` file in project root:**

```env
# Twitter API Credentials
TWITTER_API_KEY=your_consumer_key_here
TWITTER_API_SECRET=your_consumer_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
TWITTER_ENABLED=True
```

**⚠️ Important:** 
- Never commit `.env` to Git (already in `.gitignore`)
- App permissions must be **"Read and Write"** before generating tokens
- Regenerate tokens if you change permissions

### 6. Database Migration

```sh
cd eCommerce
python manage.py migrate
```

### 7. Create Superuser

```sh
python manage.py createsuperuser
# Enter: username, email, password
```

### 8. Create User Groups

**Run Django shell:**

```sh
python manage.py shell
```

**Create groups:**

```python
from django.contrib.auth.models import Group
Group.objects.create(name='Vendors')
Group.objects.create(name='Buyers')
exit()
```

### 9. Run Server

```sh
python manage.py runserver
```

Visit: http://localhost:8000

---

## User Roles

### Vendors
**Can:**
- Create and manage stores
- Add, edit, delete products
- Set product prices and stock
- Activate/deactivate stores and products
- **Use REST API to manage stores and products**
- **Auto-tweet when creating stores/products**

**Cannot:**
- Purchase products
- Add items to cart
- Leave reviews

### Buyers
**Can:**
- Browse products from all stores
- Add products to cart
- Complete checkout
- View order history
- Leave reviews (verified if purchased)
- Edit/delete own reviews
- **Access public REST API endpoints**

**Cannot:**
- Create stores
- Add/edit products

---

## REST API Documentation

### Authentication
API uses **HTTP BasicAuth**. Include credentials in request headers:

```sh
# Example with curl
curl -u username:password http://localhost:8000/api/stores/
```

### Base URL
```
http://localhost:8000/api/
```

### Endpoints

#### **Public Endpoints** (No Authentication Required)

**Get All Stores**
```http
GET /api/stores/
```
Returns list of all stores with vendor information.

**Get All Products**
```http
GET /api/products/
```
Returns list of all products with store and category details.

**Get All Categories**
```http
GET /api/categories/
```
Returns list of all product categories.

**Get Product Reviews**
```http
GET /api/reviews/
```
Returns all product reviews with verified status.

#### **Protected Endpoints** (Authentication Required)

**Create Store**
```http
POST /api/stores/add/
Content-Type: application/json

{
    "name": "My Store",
    "description": "Store description"
}
```
- Requires vendor authentication
- Auto-tweets store announcement
- Returns created store data

**Create Product**
```http
POST /api/products/add/
Content-Type: multipart/form-data

{
    "name": "Product Name",
    "store": 1,
    "category": 1,
    "description": "Product description",
    "price": "99.99",
    "stock": 50,
    "image": [file]
}
```
- Requires vendor authentication
- Auto-tweets product with image (if provided)
- Returns created product data

### Response Formats

**Success Response (200/201):**
```json
{
    "id": 1,
    "name": "Example",
    "description": "Description",
    "created_at": "2026-01-01T12:00:00Z"
}
```

**Error Response (400/401/403):**
```json
{
    "error": "Error message"
}
```

### Example API Calls

**Python requests:**
```python
import requests

# Get all stores
response = requests.get('http://localhost:8000/api/stores/')
stores = response.json()

# Create store (with auth)
auth = ('username', 'password')
data = {'name': 'My Store', 'description': 'Great products'}
response = requests.post(
    'http://localhost:8000/api/stores/add/',
    json=data,
    auth=auth
)
```

**JavaScript fetch:**
```javascript
// Get all products
fetch('http://localhost:8000/api/products/')
    .then(response => response.json())
    .then(data => console.log(data));

// Create product (with auth)
const credentials = btoa('username:password');
fetch('http://localhost:8000/api/products/add/', {
    method: 'POST',
    headers: {
        'Authorization': `Basic ${credentials}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name: 'Product',
        store: 1,
        category: 1,
        description: 'Description',
        price: '29.99',
        stock: 100
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## Twitter Integration

### Features
- **Auto-tweet on store creation**: Posts store name, description, hashtags
- **Auto-tweet on product creation**: Posts product name, store, description, price, image
- **Auto-tweet on product update**: Deletes old tweet, posts new one with updated info
- **Auto-delete tweets**: Removes tweets when stores/products are deleted
- **Background processing**: Non-blocking operations for fast page loads
- **Image support**: Automatically uploads and attaches product images to tweets

### Tweet Formats

**Store Tweet:**
```
🏪 NEW STORE: [Store Name]

[Store Description]

#eCommerce #NewStore
```

**Product Tweet:**
```
🆕 NEW PRODUCT: [Product Name]
Available at: [Store Name]

[Product Description]

💰 Price: $[Price]
#Product #Shopping

[Attached Image if available]
```

### Configuration

**Enable/Disable Twitter:**
Edit `.env` file:
```env
TWITTER_ENABLED=True   # Enable tweeting
TWITTER_ENABLED=False  # Disable tweeting
```

**Twitter API Costs:**
- Pay-per-use tier: 1,500 free requests/month
- Additional requests: charged per API call
- Check https://developer.twitter.com/en/pricing

### Troubleshooting Twitter

**403 Forbidden Error:**
- App permissions must be **"Read and Write"**
- Regenerate Access Token **after** changing permissions

**401 Unauthorized:**
- Check credentials in `.env` file
- Ensure no extra spaces in credentials

**Duplicate Tweet Error:**
- Twitter blocks identical tweets within short timeframe
- Change product/store name or description slightly

---

## Key Features Explained

### Stock Management
**Three-tier system:**
- **Out of Stock (0):** Red badge, cannot purchase
- **In Store Only (1-10):** Orange badge, limited stock
- **In Stock (11+):** Green badge, readily available

### Review System
**Two types:**
- **Verified:** User has purchased the product (green badge)
- **Unverified:** User has not purchased (yellow badge)
- Auto-verification based on order history

### Shopping Cart
- Session-based (persists after logout)
- Real-time stock validation
- Cart badge shows item count
- 10-minute session timeout

### Email System
**Development mode:** Emails saved to `emails/` folder
**Production mode:** Configure SMTP in settings

### Password Reset
- Token-based (SHA-1 hash)
- 5-minute expiration
- One-time use
- Email delivery

### Social Media Integration
- Automatic Twitter posting
- Background threading for performance
- Image upload support
- Tweet tracking with `tweet_id`
- Auto-cleanup on deletion

---

## Testing

### Run All Tests

```sh
python manage.py test
```

### Run Specific Test File

```sh
python manage.py test tests.test_authentication
python manage.py test tests.test_cart_checkout
```

### Test Coverage
- **139 automated tests** across 6 categories
- Authentication tests (16)
- Store management tests (17)
- Product management tests (25)
- Cart & checkout tests (28)
- Review system tests (23)
- Security & permissions tests (30)

### Manual Testing
See `Planning/tests/` for detailed manual test cases with step-by-step instructions.

### API Testing
Use Postman or curl to test REST endpoints:

```sh
# Test public endpoint
curl http://localhost:8000/api/stores/

# Test protected endpoint
curl -u username:password http://localhost:8000/api/stores/add/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Store","description":"Test"}'
```

---

## Admin Panel

Access: http://localhost:8000/admin/

**Manage:**
- Users and groups
- Stores and products
- Orders and order items
- Reviews
- Categories
- Password reset tokens

---

## Web Endpoints

### Public (No Login Required)
- `/` - Product list
- `/product/<id>/` - Product detail
- `/category/` - Category list
- `/category/<id>/` - Category detail
- `/stores/` - Store list
- `/store/<id>/` - Store detail

### Buyer-Only
- `/cart/` - Shopping cart
- `/cart/add/<id>/` - Add to cart
- `/cart/update/<id>/` - Update quantity
- `/cart/remove/<id>/` - Remove item
- `/checkout/` - Checkout
- `/orders/` - Order history
- `/product/<id>/review/` - Leave review
- `/review/<id>/edit/` - Edit review
- `/review/<id>/delete/` - Delete review

### Vendor-Only
- `/vendor/stores/` - Store list
- `/vendor/store/new/` - Create store
- `/vendor/store/<id>/edit/` - Edit store
- `/vendor/store/<id>/delete/` - Delete store
- `/vendor/products/` - Product list
- `/vendor/product/new/` - Add product
- `/vendor/product/<id>/edit/` - Edit product
- `/vendor/product/<id>/delete/` - Delete product
- `/vendor/categories/` - Category management

### Authentication
- `/accounts/register/` - Register
- `/accounts/login/` - Login
- `/accounts/logout/` - Logout
- `/accounts/password-reset/` - Request reset
- `/accounts/password-reset/<token>/` - Reset password

---

## Configuration

### Database Settings
**File:** `eCommerce/settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'USER': 'ecommerce_user',
        'PASSWORD': 'ecommerce_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Twitter Settings
**File:** `eCommerce/settings.py`

```python
import os
from dotenv import load_dotenv

load_dotenv()

TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
TWITTER_ENABLED = os.getenv('TWITTER_ENABLED', 'True') == 'True'
```

### Email Settings
**Development:**

```python
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'emails'
```

**Production:**

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

### Session Settings

```python
SESSION_COOKIE_AGE = 600  # 10 minutes
SESSION_SAVE_EVERY_REQUEST = True
```

### REST Framework Settings

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}
```

---

## Security Features

- ✅ Password hashing (PBKDF2_SHA256)
- ✅ CSRF protection on all forms
- ✅ XSS prevention (auto-escaping)
- ✅ SQL injection prevention (Django ORM)
- ✅ Session security (HTTP-only cookies)
- ✅ Permission-based access control
- ✅ Ownership validation
- ✅ Token expiration (password reset)
- ✅ File upload validation
- ✅ Transaction management (checkout)
- ✅ API BasicAuth authentication
- ✅ Environment variable protection (.env, .gitignore)
- ✅ Secure credential management

---

## Deployment Checklist

**Before production:**
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use HTTPS (SSL certificate)
- [ ] Set `SECURE_COOKIE_SECURE = True`
- [ ] Configure real SMTP email
- [ ] Set up daily database backups
- [ ] Use environment variables for all secrets
- [ ] Configure static file serving (collectstatic)
- [ ] Set up proper logging
- [ ] Enable rate limiting
- [ ] Configure CORS for API (if needed)
- [ ] Set up Twitter API monitoring
- [ ] Review Twitter API costs

---

## Troubleshooting

### Server Won't Start
**Issue:** "No module named 'django'"
**Solution:** Activate virtual environment

```sh
myenv\Scripts\activate  # Windows
source myenv/bin/activate  # Linux/Mac
```

### Database Connection Error
**Issue:** Can't connect to MariaDB
**Solution:** 
1. Check MariaDB is running
2. Verify database credentials in `settings.py`
3. Test connection: `mysql -u ecommerce_user -p ecommerce_db`

### Twitter API Errors
**Issue:** 403 Forbidden
**Solution:**
1. Go to Twitter Developer Portal
2. Set app permissions to **"Read and Write"**
3. Regenerate Access Token and Secret **after** permission change
4. Update `.env` file with new credentials
5. Restart Django server

**Issue:** 401 Unauthorized
**Solution:**
1. Check `.env` file exists
2. Verify no extra spaces in credentials
3. Ensure `python-dotenv` is installed
4. Restart server after changing `.env`

### Tests Failing
**Issue:** Test database errors
**Solution:** Run migrations first

```sh
python manage.py migrate
```

### Images Not Displaying
**Issue:** Uploaded images not showing
**Solution:** Check `MEDIA_URL` and `MEDIA_ROOT` in `settings.py`

### API Not Working
**Issue:**
