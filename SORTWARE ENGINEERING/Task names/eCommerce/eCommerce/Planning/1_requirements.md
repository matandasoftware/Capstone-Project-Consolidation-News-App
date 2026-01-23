# 1. SYSTEM REQUIREMENTS

## Project Overview
eCommerce web application built with Django that allows users to register as Vendors (sellers) or Buyers (customers).

---

## User Types

### 1. VENDORS
**Who:** People who want to sell products online

**What they can do:**
- Create and manage their own stores
- Add products to their stores (with images, prices, stock)
- Edit product information
- Delete products
- Set product availability (active/inactive)
- View all their products across stores

**What they CANNOT do:**
- Purchase products
- Add items to cart
- Leave reviews

---

### 2. BUYERS
**Who:** Customers who want to shop

**What they can do:**
- Browse all products from different vendors
- Add products to shopping cart
- Update cart quantities
- Remove items from cart
- Complete checkout
- View order history
- Leave product reviews (verified if purchased)
- Edit/delete their own reviews

**What they CANNOT do:**
- Create stores
- Add/edit products

---

### 3. ANONYMOUS USERS
**Who:** Visitors without accounts

**What they can do:**
- View products
- View categories

**What they CANNOT do:**
- Add to cart
- Purchase
- Leave reviews

---

## Core Features Built

### Authentication System
- User registration (choose Vendor or Buyer)
- Login/logout
- Password reset via email (5-minute token expiration)
- Session management (10-minute timeout)

### Store Management (Vendors)
- Create store (name, description, active status)
- View all owned stores
- Edit store information
- Delete stores (with confirmation)

### Product Management (Vendors)
- Add products (name, price, stock, image, category)
- Stock levels:
  - 0 = Out of Stock (red)
  - 1-10 = In Store Only (orange)
  - 11+ = In Stock (green)
- Edit products
- Delete products
- Only manage products in owned stores

### Shopping Cart (Buyers)
- Session-based cart (persists after logout)
- Add products to cart
- Update quantities
- Remove items
- View cart total
- Stock validation

### Checkout & Orders
- Review order before purchase
- Create order records
- Generate invoice (HTML email)
- Send invoice to buyer's email
- Reduce product stock automatically
- Clear cart after purchase

### Review System (Buyers)
- Leave reviews (1-5 stars, comment)
- **Verified reviews:** User purchased the product (green badge)
- **Unverified reviews:** User didn't purchase (yellow badge)
- Auto-verification based on purchase history
- One review per user per product
- Edit/delete own reviews

### Email System
- Password reset emails (with expiring tokens)
- Order invoices
- File-based storage (development)

### Database
- MariaDB 10.6 backend
- All data stored in relational database
- Foreign key relationships enforced

### Security
- Password hashing (PBKDF2)
- CSRF protection
- Permission checks (vendors/buyers separated)
- Ownership validation (can only edit own content)

---

## Technology Stack

**Backend:**
- Python 3.12
- Django 6.0
- MariaDB 10.6

**Frontend:**
- HTML5
- CSS3
- Bootstrap 5 (responsive design)

**Key Libraries:**
- mysqlclient (database connector)
- Pillow (image handling)

---

## Requirements Met

✅ Users register as Vendor or Buyer
✅ Vendors create/manage stores and products
✅ Buyers view products, add to cart, checkout
✅ Session-based cart tracking
✅ Invoice emailed after checkout
✅ Verified/unverified review system
✅ Password reset with expiring tokens
✅ MariaDB database
✅ Authentication and permissions enforced

---

## Constraints

- No payment processing (future feature)
- No shipping calculator
- Single currency (South African Rand)
- Email stored as files (development mode)
- No product search functionality

## Project Overview
**eCommerce Web Application** - A Django-based platform allowing users to register as Vendors or Buyers, enabling product sales and purchases.

---

## User Types & Requirements

### 1. VENDORS
**Purpose:** Sell products through online stores

**Functional Requirements:**
- Must register with "Vendor" account type
- Can create multiple stores
- Can manage stores (create, view, edit, delete)
- Can add products to their stores
- Can manage products (create, view, edit, delete)
- Can set product prices, stock levels, and descriptions
- Can upload product images
- Can activate/deactivate stores and products
- Cannot purchase products (buyers only)
- Cannot leave reviews

**User Stories:**
- As a vendor, I want to create a store so I can sell products online
- As a vendor, I want to add products with images and prices
- As a vendor, I want to manage my inventory by updating stock levels
- As a vendor, I want to edit my store information
- As a vendor, I want to deactivate products temporarily without deleting them

---

### 2. BUYERS
**Purpose:** Browse and purchase products from various vendors

**Functional Requirements:**
- Must register with "Buyer" account type
- Can view all active products from all stores
- Can add products to shopping cart (session-based)
- Can update cart quantities
- Can remove items from cart
- Can complete checkout process
- Can view order history
- Can leave reviews (verified if purchased, unverified otherwise)
- Can edit/delete own reviews
- Receive invoice via email after purchase
- Cannot create stores or products

**User Stories:**
- As a buyer, I want to browse products from different vendors
- As a buyer, I want to add multiple products to my cart
- As a buyer, I want to checkout and receive an email invoice
- As a buyer, I want to leave reviews for products
- As a buyer, I want my verified purchase reviews to be marked as trusted
- As a buyer, I want to view my order history

---

### 3. ANONYMOUS USERS
**Purpose:** Browse products without account

**Functional Requirements:**
- Can view products (read-only)
- Can view categories
- Cannot add to cart
- Cannot checkout
- Cannot leave reviews
- Must register to purchase

---

## Functional Requirements by Module

### A. AUTHENTICATION SYSTEM
1. **User Registration**
   - Username (unique, 3-150 chars)
   - Email (unique, valid format)
   - Password (min 8 chars, hashed)
   - Account type selection (Vendor/Buyer)
   - Automatic group assignment

2. **User Login**
   - Username/password authentication
   - Session creation
   - Remember user across pages
   - Auto-logout after inactivity (10 min)

3. **Password Reset**
   - Email-based reset link
   - Secure token generation (SHA-1 hashed)
   - Token expiration (5 minutes)
   - One-time use tokens

4. **Permissions**
   - Group-based access control (Vendors/Buyers)
   - View-level permissions
   - Model-level permissions

---

### B. STORE MANAGEMENT (Vendors Only)
1. **Create Store**
   - Name (required, max 255 chars)
   - Description (text)
   - Active status (boolean)
   - Automatic vendor assignment

2. **View Stores**
   - List all owned stores
   - Show product count per store
   - Show store status (active/inactive)
   - Sort by creation date

3. **Edit Store**
   - Update name and description
   - Toggle active status
   - Ownership validation

4. **Delete Store**
   - Confirmation required
   - Cascade delete (removes all products)
   - Cannot be undone warning

---

### C. PRODUCT MANAGEMENT
**Vendors:**
1. **Add Product**
   - Name (required)
   - Store selection (only owned stores)
   - Category (optional)
   - Description (required)
   - Price (decimal, Rands)
   - Stock quantity (integer, ≥0)
   - Image upload (optional)
   - Active status

2. **Stock Management**
   - Three-tier system:
     - Out of Stock (0 items) - Red badge
     - In Store Only (1-10 items) - Orange badge
     - In Stock (11+ items) - Green badge
   - Automatic reduction after purchase

3. **Edit/Delete Product**
   - Ownership validation
   - Cannot edit products in other vendors' stores

**Buyers:**
- View all active products
- Filter by category
- View product details
- See store information
- Cannot modify products

---

### D. SHOPPING CART SYSTEM (Buyers Only)
1. **Session-Based Cart**
   - Persists during browsing
   - Survives page refresh
   - Preserved after logout (optional)
   - 10-minute inactivity timeout

2. **Cart Operations**
   - Add product (single unit)
   - Update quantity
   - Remove item
   - View total
   - Cart badge shows item count

3. **Stock Validation**
   - Cannot add more than available stock
   - Real-time stock checking
   - Warning messages for insufficient stock

---

### E. CHECKOUT & ORDERS
1. **Checkout Process**
   - Review cart items
   - Confirm buyer details
   - Create order record
   - Generate order items
   - Reduce product stock
   - Clear cart

2. **Order Model**
   - Buyer reference
   - Order date (auto)
   - Total amount
   - Status (pending, paid, shipped, delivered, cancelled)
   - Related order items

3. **Invoice Generation**
   - HTML invoice template
   - Order summary
   - Itemized list
   - Total calculation
   - Email delivery (file-based for dev)

---

### F. REVIEW SYSTEM (Buyers Only)
1. **Review Types**
   - **Verified:** User has purchased the product
   - **Unverified:** User has not purchased

2. **Review Features**
   - Star rating (1-5)
   - Comment (required)
   - Auto-verification (checks purchase history)
   - One review per user per product
   - Edit own reviews
   - Delete own reviews

3. **Review Display**
   - Verified reviews appear first
   - Show verification badge
   - Show reviewer username
   - Show review date
   - Star rating visualization

---

## Non-Functional Requirements

### Performance
- Page load time: < 2 seconds
- Support 100 concurrent users
- Database queries optimized

### Security
- Passwords hashed (PBKDF2)
- CSRF protection enabled
- XSS protection (Django auto-escape)
- SQL injection prevention (Django ORM)
- Session security (HTTP-only cookies)
- Password reset token expiration

### Scalability
- Database: MariaDB (production)
- Session storage: Database-backed
- Static files: Separate storage capability
- Media files: Upload directory

### Reliability
- Error handling for all views
- User-friendly error messages
- Form validation (client & server)
- Stock validation before checkout

### Usability
- Responsive design (Bootstrap 5)
- Intuitive navigation
- Clear success/error messages
- Consistent UI across pages

---

## Technical Requirements

### Technology Stack
- **Backend:** Django 6.0+
- **Database:** MariaDB 10.6
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Language:** Python 3.12
- **Email:** File-based (dev) / SMTP (prod)
- **Authentication:** Django built-in
- **Session Management:** Django session framework

### Dependencies
```
Django==6.0+
mysqlclient
Pillow (image handling)
```

### Browser Compatibility
- Chrome (latest)
- Firefox (latest)
- Edge (latest)
- Safari (latest)

---

## Data Requirements

### Storage
- Product images: Max 5MB per image
- Supported formats: JPG, PNG, GIF
- User data: Encrypted in database

### Backup
- Database backups: Daily (production)
- Retention: 30 days

---

## Constraints & Assumptions

### Constraints
- Python 3.12+ required
- MariaDB 10.6+ required
- Internet connection for Bootstrap CDN
- Email server for production

### Assumptions
- Users have valid email addresses
- Vendors have products to sell
- Payment processing not included (future enhancement)
- Shipping/delivery not implemented
- Single currency (South African Rand)

---

## Future Enhancements (Out of Scope)
- Payment gateway integration
- Shipping calculator
- Real-time chat support
- Product search with filters
- Wish lists
- Product recommendations
- Multi-vendor shopping cart
- Advanced analytics dashboard
