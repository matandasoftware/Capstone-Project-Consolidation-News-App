# 3. ACCESS CONTROL & SECURITY

## Authentication System

### User Registration
- Username must be unique and 3-150 characters
- Email must be unique and valid format
- Password minimum 8 characters
- User chooses account type: Vendor or Buyer
- Automatic assignment to "Vendors" or "Buyers" group

### Login Security
- Django session-based authentication
- Passwords hashed using PBKDF2 with SHA256
- Session timeout after 10 minutes of inactivity
- HTTP-only cookies (JavaScript cannot access)

### Password Reset
- Token-based system via email
- Token generated using SHA-1 hash (timestamp + username)
- Token expires after 5 minutes
- One-time use (deleted after successful reset)
- Email sent with reset link

---

## Authorization & Permissions

### User Groups

**Vendors Group - Can:**
- Create, edit, delete own stores
- Add, edit, delete products in own stores
- View own products and stores

**Vendors Group - Cannot:**
- Add products to cart
- Checkout
- Leave reviews
- Edit other vendors' stores/products

**Buyers Group - Can:**
- Add products to cart
- Checkout and place orders
- View order history
- Leave reviews for products
- Edit/delete own reviews

**Buyers Group - Cannot:**
- Create stores
- Add/edit products
- Access vendor features

---

## View-Level Protection

### Public Views (No Login Required)
- Product list
- Product detail
- Category list
- Category detail

### Login Required Views
- Shopping cart
- Checkout
- Order history
- Review management
- Store management
- Product management

### Implementation
```python
@login_required  # Requires user to be logged in
@user_passes_test(is_vendor)  # Vendor-only views
@user_passes_test(is_buyer)   # Buyer-only views
```

---

## Ownership Validation

**Stores:**
- Vendors can only view/edit/delete their own stores
- Check: `store.vendor == request.user`

**Products:**
- Vendors can only manage products in their stores
- Check: `product.store.vendor == request.user`

**Reviews:**
- Users can only edit/delete their own reviews
- Check: `review.user == request.user`

**Orders:**
- Buyers can only view their own orders
- Check: `order.buyer == request.user`

---

## Data Security

### Password Security
- Never stored in plaintext
- Hashed using Django's PBKDF2_SHA256
- Salt automatically added
- Minimum length enforced (8 characters)

### SQL Injection Prevention
- Django ORM uses parameterized queries automatically
- No raw SQL used
- All user input validated

### XSS Protection
- Django auto-escapes HTML output
- User input never rendered as raw HTML
- CSRF tokens required on all POST forms

### CSRF Protection
- CSRF middleware enabled
- `{% csrf_token %}` in all forms
- Validates token on form submission

---

## File Upload Security

**Product Images:**
- Allowed formats: JPG, PNG, GIF only
- Maximum file size: 5MB
- Stored in separate media directory
- File extension validation
- No executable files allowed

---

## Session Management

### Session Configuration
```python
SESSION_COOKIE_AGE = 600  # 10 minutes
SESSION_SAVE_EVERY_REQUEST = True  # Refresh on activity
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access
```

### Session Data Stored
- User ID (for authentication)
- Shopping cart contents `{'product_id': quantity}`
- CSRF tokens

### Session Security
- Unique session ID per user
- Session cleared on logout
- Cart can optionally persist after logout

---

## Input Validation

### Server-Side Validation (Django Forms)
All forms validate:
- Required fields
- Data types (integers, decimals, text)
- Field lengths
- Format (email validation)
- Custom rules (stock ≥ 0, price > 0)

### Client-Side Validation (HTML5)
- `required` attribute on fields
- `type="email"` for emails
- `type="number"` with min/max
- `maxlength` on text fields
- Immediate feedback for users

---

## Email Security

### Password Reset Tokens
```python
token = hashlib.sha1(f"{username}{timestamp}".encode()).hexdigest()
```
- Stored in database with expiration time
- Validated before allowing password change
- Deleted after single use

### Invoice Emails
- No sensitive data in subject line
- HTML content sanitized
- File-based backend (development)
- SMTP backend (production)

---

## Access Control Matrix

| Action | Public | Buyer | Vendor | Admin |
|--------|--------|-------|--------|-------|
| View Products | ✓ | ✓ | ✓ | ✓ |
| Add to Cart | ✗ | ✓ | ✗ | ✓ |
| Checkout | ✗ | ✓ | ✗ | ✓ |
| Leave Review | ✗ | ✓ | ✗ | ✓ |
| Create Store | ✗ | ✗ | ✓ | ✓ |
| Add Product | ✗ | ✗ | ✓ | ✓ |
| Admin Panel | ✗ | ✗ | ✗ | ✓ |

---

## Security Best Practices Planned

- Passwords hashed, never stored plaintext
- CSRF protection on all forms
- XSS prevention (auto-escaping)
- SQL injection prevention (ORM)
- Session timeouts
- Ownership validation
- Group-based permissions
- HTTP-only cookies
- File upload validation
- Token expiration (password reset)
- Login required decorators

---

## Production Security Checklist

**Before deployment:**
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use HTTPS (SSL certificate)
- [ ] Set SECURE_COOKIE_SECURE = True
- [ ] Configure real SMTP email
- [ ] Enable database backups
- [ ] Keep SECRET_KEY secret
- [ ] Review all permission checks

## Authentication System

### User Registration
- Username validation (unique, 3-150 chars)
- Email validation (unique, valid format)
- Password requirements: minimum 8 characters
- Account type selection: Vendor or Buyer
- Automatic group assignment on registration

### Login Security
- Session-based authentication (Django sessions)
- Password hashing: PBKDF2 with SHA256
- Session timeout: 10 minutes of inactivity
- HTTP-only cookies (prevents XSS access)
- CSRF protection enabled on all forms

### Password Reset
- Token-based password reset
- Token generation: SHA-1 hash of timestamp + username
- Token expiration: 5 minutes
- One-time use tokens (deleted after use)
- Email delivery to registered address

---

## Authorization & Permissions

### User Groups
**Vendors Group:**
- Can create/edit/delete own stores
- Can create/edit/delete products in own stores
- Cannot purchase products
- Cannot leave reviews
- Cannot access buyer features

**Buyers Group:**
- Can add products to cart
- Can checkout and place orders
- Can leave reviews (verified if purchased)
- Cannot create stores
- Cannot add/edit products
- Cannot access vendor features

### View-Level Protection
**Public Views (no login required):**
- Product list
- Product detail
- Category list
- Category detail

**Login Required:**
- Shopping cart
- Checkout
- Order history
- Review management
- Store management (vendors)
- Product management (vendors)

**Permission Checks:**
```python
@login_required
@user_passes_test(is_vendor)  # Vendor-only views

@login_required
@user_passes_test(is_buyer)   # Buyer-only views
```

### Ownership Validation
**Stores:** Vendors can only edit/delete their own stores
**Products:** Vendors can only manage products in their stores
**Reviews:** Users can only edit/delete their own reviews
**Orders:** Buyers can only view their own orders

---

## Data Security

### Database Security
**Sensitive Data:**
- Passwords: Hashed (never stored as plaintext)
- Session data: Encrypted in database
- Personal information: Protected by Django ORM

**SQL Injection Prevention:**
- Django ORM parameterized queries
- No raw SQL queries used
- Input validation on all forms

### XSS Protection
- Django auto-escaping enabled
- HTML output sanitized automatically
- User input never rendered as raw HTML
- CSRF tokens on all POST forms

### File Upload Security
**Product Images:**
- Allowed formats: JPG, PNG, GIF only
- Max file size: 5MB
- Stored in media directory (separate from code)
- Validated file extensions
- No executable file uploads allowed

---

## Session Management

### Session Configuration
```python
SESSION_COOKIE_AGE = 600  # 10 minutes
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = True  # Prevents JavaScript access
SESSION_COOKIE_SECURE = False  # True in production (HTTPS)
```

### Session Data Stored
- User ID (for authentication)
- Shopping cart contents
- CSRF tokens
- Login timestamp

### Session Security
- Unique session ID per user
- Session regeneration on login
- Session cleared on logout
- Cart persists after logout (optional)

---

## Email Security

### Email Token System
**Password Reset Tokens:**
- Generated: `hashlib.sha1(f"{username}{timestamp}".encode()).hexdigest()`
- Stored in database with expiration
- Validated before allowing password change
- Deleted after single use

**Invoice Emails:**
- File-based backend (development)
- SMTP backend (production)
- No sensitive data in email subject
- HTML sanitization

---

## Input Validation

### Server-Side Validation
**All Forms:**
- Required field validation
- Data type validation
- Length constraints
- Format validation (email, numbers)

**Examples:**
- Username: 3-150 chars, alphanumeric
- Email: Valid email format
- Price: Decimal, positive, max 10 digits
- Stock: Integer, non-negative
- Rating: Integer, 1-5 only

### Client-Side Validation
- HTML5 form validation attributes
- Bootstrap form styling
- User-friendly error messages
- Prevents basic invalid submissions

---

## Security Best Practices

### Django Security Settings
```python
DEBUG = False  # Production only
ALLOWED_HOSTS = ['yourdomain.com']  # Production
SECRET_KEY = 'unique-secret-key'  # Keep secret!
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### Password Security
- Minimum length: 8 characters
- Hashing algorithm: PBKDF2_SHA256 (Django default)
- No password in URL parameters
- No password in logs
- Password change requires old password

### API Security (Future)
- No API currently implemented
- Future: Token-based authentication
- Rate limiting recommended
- CORS configuration needed

---

## Access Control Matrix

| Feature | Public | Buyer | Vendor | Admin |
|---------|--------|-------|--------|-------|
| View Products | ✓ | ✓ | ✓ | ✓ |
| Add to Cart | ✗ | ✓ | ✗ | ✓ |
| Checkout | ✗ | ✓ | ✗ | ✓ |
| Leave Review | ✗ | ✓ | ✗ | ✓ |
| Create Store | ✗ | ✗ | ✓ | ✓ |
| Add Product | ✗ | ✗ | ✓ | ✓ |
| View All Orders | ✗ | Own Only | ✗ | ✓ |
| Admin Panel | ✗ | ✗ | ✗ | ✓ |

---

## Security Threats & Mitigation

### Threat: Unauthorized Access
**Mitigation:**
- Login required decorators
- Permission checks on every view
- Ownership validation
- Session-based authentication

### Threat: SQL Injection
**Mitigation:**
- Django ORM (parameterized queries)
- No raw SQL
- Input validation

### Threat: XSS Attacks
**Mitigation:**
- Django auto-escaping
- CSRF protection
- HTTP-only cookies
- Content Security Policy headers

### Threat: CSRF Attacks
**Mitigation:**
- CSRF tokens on all forms
- Django middleware enabled
- Token validation on POST

### Threat: Brute Force Login
**Mitigation:**
- Strong password requirements
- Session timeout
- Future: Rate limiting, account lockout

### Threat: Session Hijacking
**Mitigation:**
- HTTP-only cookies
- Session regeneration
- Short session timeout
- HTTPS in production

### Threat: File Upload Exploits
**Mitigation:**
- File type validation
- Size limits
- Separate media directory
- No executable permissions

---

## Compliance & Privacy

### Data Protection
- User consent for data collection (registration)
- Password reset requires email verification
- Users can delete own reviews
- No data sold to third parties

### Audit Trail
**Logged Actions:**
- User registration
- Login attempts (future)
- Order creation
- Review submission
- Store/product changes (via Django admin)

**Not Logged:**
- Passwords (only hashed)
- Session data (temporary)
- Cart contents (session-based)

---

## Production Security Checklist

**Before Deployment:**
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use HTTPS (SSL certificate)
- [ ] Set SECURE_COOKIE = True
- [ ] Configure SMTP email backend
- [ ] Enable database backups
- [ ] Review SECRET_KEY security
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Enable logging
- [ ] Review file upload permissions
- [ ] Test password reset flow
- [ ] Verify CSRF protection
- [ ] Test permission boundaries
