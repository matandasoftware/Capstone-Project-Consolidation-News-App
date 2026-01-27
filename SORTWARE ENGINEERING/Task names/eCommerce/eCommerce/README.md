# eCommerce Web Application

Django-based multi-vendor eCommerce platform with role-based access control.

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
- MariaDB database backend
- Responsive Bootstrap 5 UI

---

## Technology Stack

**Backend:**
- Python 3.12
- Django 6.0
- MariaDB 10.6

**Frontend:**
- HTML5/CSS3
- Bootstrap 5
- Django Templates

**Key Libraries:**
- mysqlclient (database)
- Pillow (image handling)

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
│   ├── models.py         # Store, Product, Order, Review
│   ├── views.py          # All business logic
│   ├── forms.py          # Product, store, review forms
│   ├── admin.py          # Django admin config
│   ├── tests.py          # Product tests
│   ├── templates/        # HTML templates
│   └── templatetags/     # Custom template tags
├── eCommerce/            # Project settings
│   ├── settings.py       # Django configuration
│   ├── urls.py           # Root URL config
│   └── tests/            # Automated test suite
│       ├── test_authentication.py
│       ├── test_store_management.py
│       ├── test_product_management.py
│       ├── test_cart_checkout.py
│       ├── test_review_system.py
│       └── test_security_permissions.py
├── Planning/             # Documentation
│   ├── 1_requirements.md
│   ├── 2_ui_layout.md
│   ├── 3_access_control.md
│   ├── 4_failure_handling.md
│   ├── 5_database_schema.md
│   ├── 6_test_cases.md
│   └── tests/            # Manual test documentation
│       ├── index.md
│       ├── authentication.md
│       ├── store_management.md
│       ├── product_management.md
│       ├── cart_checkout.md
│       ├── review_system.md
│       └── security_permissions.md
├── emails/               # Email storage (development)
├── media/                # Uploaded product images
├── static/               # CSS, JS, images
└── manage.py             # Django management script
```

---

## Setup Instructions

### 1. Prerequisites

- Python 3.12+
- MariaDB 10.6+
- pip (Python package manager)

### 2. Database Setup

**Start MariaDB:**
```bash
# Windows
net start mariadb

# Linux/Mac
sudo systemctl start mariadb
```

**Create database:**
```bash
mysql -u root -p

CREATE DATABASE ecommerce_db;
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'ecommerce_password';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Virtual Environment

**Create and activate:**
```bash
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

```bash
pip install django
pip install mysqlclient
pip install Pillow
```

### 5. Database Migration

```bash
cd eCommerce
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
# Enter: username, email, password
```

### 7. Create User Groups

**Run Django shell:**
```bash
python manage.py shell
```

**Create groups:**
```python
from django.contrib.auth.models import Group
Group.objects.create(name='Vendors')
Group.objects.create(name='Buyers')
exit()
```

### 8. Run Server

```bash
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

**Cannot:**
- Create stores
- Add/edit products

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

---

## Testing

### Run All Tests
```bash
python manage.py test
```

### Run Specific Test File
```bash
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

## API Endpoints

### Public (No Login Required)
- `/` - Product list
- `/product/<id>/` - Product detail
- `/category/` - Category list
- `/category/<id>/` - Category detail

### Buyer-Only
- `/cart/` - Shopping cart
- `/cart/add/<id>/` - Add to cart
- `/cart/update/<id>/` - Update quantity
- `/cart/remove/<id>/` - Remove item
- `/checkout/` - Checkout
- `/orders/` - Order history
- `/product/<id>/review/` - Leave review

### Vendor-Only
- `/stores/` - Store list
- `/store/new/` - Create store
- `/store/<id>/edit/` - Edit store
- `/store/<id>/delete/` - Delete store
- `/vendor/products/` - Product list
- `/vendor/product/new/` - Add product
- `/vendor/product/<id>/edit/` - Edit product
- `/vendor/product/<id>/delete/` - Delete product

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

---

## Deployment Checklist

**Before production:**
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use HTTPS (SSL certificate)
- [ ] Set `SECURE_COOKIE_SECURE = True`
- [ ] Configure real SMTP email
- [ ] Set up daily database backups
- [ ] Use environment variables for secrets
- [ ] Configure static file serving
- [ ] Set up proper logging
- [ ] Enable rate limiting

---

## Troubleshooting

### Server Won't Start
**Issue:** "No module named 'django'"
**Solution:** Activate virtual environment
```bash
myenv\Scripts\activate  # Windows
source myenv/bin/activate  # Linux/Mac
```

### Database Connection Error
**Issue:** Can't connect to MariaDB
**Solution:** 
1. Check MariaDB is running
2. Verify database credentials in `settings.py`
3. Test connection: `mysql -u ecommerce_user -p ecommerce_db`

### Tests Failing
**Issue:** Test database errors
**Solution:** Run migrations first
```bash
python manage.py migrate
```

### Images Not Displaying
**Issue:** Uploaded images not showing
**Solution:** Check `MEDIA_URL` and `MEDIA_ROOT` in `settings.py`

---

## Documentation

**Planning Documents:**
- Requirements specification
- UI/UX layout plan
- Access control & security
- Failure handling & error recovery
- Database schema
- Test cases overview

**Test Documentation:**
- 139 manual test cases
- 6 test categories
- Step-by-step instructions
- Expected results
- Pass/fail tracking

**Location:** `Planning/` folder

---

## Contributing

This is a capstone project for academic purposes.

---

## License

Academic project - All rights reserved.

---

## Author

**Student:** [Your Name]
**Institution:** [Your Institution]
**Year:** 2026
**Project:** Capstone - eCommerce Web Application

---

## Acknowledgments

- Django framework
- Bootstrap 5
- MariaDB
- Python community

---

## Support

For issues or questions:
1. Check `Planning/` documentation
2. Review test cases in `Planning/tests/`
3. Check Django logs
4. Review error messages carefully

---

**Project Status:** ✅ Complete and ready for submission!
