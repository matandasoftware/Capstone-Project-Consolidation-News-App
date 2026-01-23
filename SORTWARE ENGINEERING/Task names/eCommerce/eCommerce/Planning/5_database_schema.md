# 5. DATABASE SCHEMA

## Database Setup

**Engine:** MariaDB 10.6
**Database Name:** ecommerce_db
**Character Set:** UTF8MB4 (supports international characters and emojis)
**User:** ecommerce_user

---

## Core Tables

### 1. auth_user (Django Built-in - Users)
Stores all user accounts (vendors and buyers)

**Key Fields:**
- `id` - Primary key
- `username` - Unique login name
- `email` - Unique email address
- `password` - Hashed password (PBKDF2)
- `is_staff` - Admin access flag
- `is_active` - Account status
- `date_joined` - Registration timestamp

---

### 2. auth_group (Django Built-in - User Groups)
Groups for permission management

**Data:**
- Vendors
- Buyers

---

### 3. auth_user_groups (Django Built-in - Group Membership)
Links users to their groups (many-to-many)

**Key Fields:**
- `user_id` - Reference to user
- `group_id` - Reference to group (Vendors or Buyers)

---

### 4. accounts_resettoken (Password Reset Tokens)
Manages password reset tokens

**Key Fields:**
- `id` - Primary key
- `user_id` - Foreign key to user
- `token` - SHA-1 hash (unique)
- `created_at` - Token creation time
- `expires_at` - Expiration time (5 minutes after creation)
- `used` - Boolean flag (prevents reuse)

**Cleanup:** Tokens deleted after use

---

### 5. product_category (Product Categories)
Product categories for organization

**Key Fields:**
- `id` - Primary key
- `name` - Category name (unique)
- `description` - Category description
- `created_at` - Timestamp
- `updated_at` - Last modified timestamp

**Example Data:** Electronics, Clothing, Books

---

### 6. product_store (Vendor Stores)
Stores owned by vendors

**Key Fields:**
- `id` - Primary key
- `vendor_id` - Foreign key to user (owner)
- `name` - Store name
- `description` - Store description
- `is_active` - Active/inactive flag
- `created_at` - Creation timestamp
- `updated_at` - Last modified timestamp

**Relationships:** One vendor can have many stores

---

### 7. product_product (Products)
Products for sale

**Key Fields:**
- `id` - Primary key
- `store_id` - Foreign key to store
- `category_id` - Foreign key to category (nullable)
- `name` - Product name
- `description` - Product description
- `price` - Decimal(10,2) in Rands
- `stock` - Integer (available quantity)
- `image` - File path (nullable)
- `is_active` - Active/inactive flag
- `created_at` - Timestamp
- `updated_at` - Last modified timestamp

**Stock Rules:**
- 0 = Out of Stock (red badge)
- 1-10 = In Store Only (orange badge)
- 11+ = In Stock (green badge)

**Relationships:**
- One store can have many products
- One category can have many products

---

### 8. product_order (Customer Orders)
Orders placed by buyers

**Key Fields:**
- `id` - Primary key (Order number)
- `buyer_id` - Foreign key to user (buyer)
- `total_amount` - Decimal(10,2) total cost
- `status` - Order status (pending/paid/shipped/delivered/cancelled)
- `order_date` - Auto-generated timestamp

**Relationships:** One buyer can have many orders

---

### 9. product_orderitem (Order Items)
Individual products within orders

**Key Fields:**
- `id` - Primary key
- `order_id` - Foreign key to order
- `product_id` - Foreign key to product
- `quantity` - Number ordered
- `price` - Decimal(10,2) price at purchase time

**Important:** Price stored at purchase time (preserves history if product price changes later)

**Relationships:**
- One order can have many items
- One product can be in many orders

---

### 10. product_review (Product Reviews)
Reviews left by buyers

**Key Fields:**
- `id` - Primary key
- `product_id` - Foreign key to product
- `user_id` - Foreign key to user (reviewer)
- `rating` - Integer (1-5 stars)
- `comment` - Text review
- `verified` - Boolean (purchased or not)
- `created_at` - Review timestamp

**Unique Constraint:** One review per user per product

**Verification Logic:**
- Automatically set when saved
- Checks if user has OrderItem for this product
- If yes: verified = True (green badge)
- If no: verified = False (yellow badge)

**Relationships:**
- One product can have many reviews
- One user can review many products (but only once per product)

---

## Relationships Summary

```
User
├── Has many Stores (if vendor)
├── Has many Orders (if buyer)
└── Has many Reviews

Store
├── Belongs to one Vendor (User)
└── Has many Products

Product
├── Belongs to one Store
├── Belongs to one Category (optional)
├── Has many OrderItems
└── Has many Reviews

Order
├── Belongs to one Buyer (User)
└── Has many OrderItems

OrderItem
├── Belongs to one Order
└── References one Product

Review
├── Belongs to one Product
└── Written by one User

Category
└── Has many Products
```

---

## Key Database Features

### Foreign Key Constraints
**Cascading Deletes:**
- Delete Store → All products in store deleted
- Delete Order → All order items deleted
- Delete Product → All reviews deleted
- Delete User → Reviews deleted, Orders remain

**Protection:**
- Cannot delete Product if it's in any order (PROTECT constraint)

### Unique Constraints
- Username (unique across all users)
- Email (unique across all users)
- Reset token (unique)
- Review per user per product (unique together)

### Indexes
- Primary keys (automatic)
- Foreign keys (automatic)
- Email, username for login lookups
- Active flags for filtering
- Order date for sorting

---

## Session Storage

**Table:** django_session

**Purpose:** Store user sessions (cart, login state)

**Data Stored:**
- Session ID (unique key)
- User ID (if logged in)
- Cart contents `{'product_id': quantity}`
- CSRF tokens

**Expiration:** 10 minutes of inactivity

---

## Migration from SQLite to MariaDB

**Process Completed:**
1. ✓ Installed MariaDB 10.6
2. ✓ Created database `ecommerce_db`
3. ✓ Created user `ecommerce_user` with password
4. ✓ Updated Django settings.py
5. ✓ Ran `python manage.py migrate`
6. ✓ Created superuser

**Result:** Fresh MariaDB database with all tables created

---

## Database Configuration

**Django Settings:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'USER': 'ecommerce_user',
        'PASSWORD': 'ecommerce_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}
```

---

## Data Integrity

**Maintained Through:**
- Foreign key constraints
- Unique constraints
- NOT NULL requirements
- Check constraints (stock ≥ 0, price > 0)
- Transaction management (checkout process)
- Django ORM validation

---

## Backup Strategy (Production)

**Recommended:**
- Daily automated backups
- Retention: 30 days
- Store in separate location
- Test restore procedure

**Command:**
```bash
mysqldump -u ecommerce_user -p ecommerce_db > backup.sql
```

## Database Overview

**Database Engine:** MariaDB 10.6
**Character Set:** UTF8MB4 (supports emojis, international chars)
**Collation:** utf8mb4_unicode_ci

---

## Core Tables

### 1. auth_user (Django Built-in)
**Purpose:** Store user accounts

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO_INCREMENT | User ID |
| username | VARCHAR(150) | UNIQUE, NOT NULL | Login username |
| email | VARCHAR(254) | UNIQUE, NOT NULL | User email |
| password | VARCHAR(128) | NOT NULL | Hashed password |
| first_name | VARCHAR(150) | | Optional |
| last_name | VARCHAR(150) | | Optional |
| is_staff | BOOLEAN | DEFAULT FALSE | Admin access |
| is_superuser | BOOLEAN | DEFAULT FALSE | Full permissions |
| is_active | BOOLEAN | DEFAULT TRUE | Account status |
| date_joined | DATETIME | AUTO | Registration date |

**Indexes:**
- PRIMARY KEY (id)
- UNIQUE (username)
- UNIQUE (email)

---

### 2. auth_group (Django Built-in)
**Purpose:** User groups (Vendors, Buyers)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO_INCREMENT | Group ID |
| name | VARCHAR(150) | UNIQUE, NOT NULL | Group name |

**Data:**
- Vendors
- Buyers

---

### 3. auth_user_groups (Django Built-in)
**Purpose:** Many-to-many relationship between users and groups

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO_INCREMENT | Relation ID |
| user_id | INTEGER | FK(auth_user.id) | User reference |
| group_id | INTEGER | FK(auth_group.id) | Group reference |

**Indexes:**
- UNIQUE (user_id, group_id)
- INDEX (user_id)
- INDEX (group_id)

---

### 4. accounts_resettoken
**Purpose:** Password reset tokens

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO_INCREMENT | Token ID |
| user_id | INTEGER | FK(auth_user.id) | User reference |
| token | VARCHAR(64) | UNIQUE, NOT NULL | SHA-1 hash |
| created_at | DATETIME | AUTO | Token creation time |
| expires_at | DATETIME | NOT NULL | Expiration time (5 min) |
| used | BOOLEAN | DEFAULT FALSE | Usage status |

**Indexes:**
- PRIMARY KEY (id)
- UNIQUE (token)
- INDEX (user_id)
- INDEX (expires_at)

**Cleanup:** Expired tokens deleted after use

---

### 5. product_category
**Purpose:** Product categories

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO_INCREMENT | Category ID |
| name | VARCHAR(255) | UNIQUE, NOT NULL | Category name |
| description | TEXT | | Category description |
| created_at | DATETIME | AUTO | Creation timestamp |
| updated_at | DATETIME | AUTO_UPDATE | Last update timestamp |

**Indexes:**
- PRIMARY KEY (id)
- UNIQUE (name)

**Example Data:**
- Electronics
- Clothing
- Books
- Home & Garden

---

### 6. product_store
**Purpose:** Vendor stores

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO_INCREMENT | Store ID |
| vendor_id | INTEGER | FK(auth_user.id) | Owner (vendor) |
| name | VARCHAR(255) | NOT NULL | Store name |
| description | TEXT | | Store description |
| is_active | BOOLEAN | DEFAULT TRUE | Store status |
| created_at | DATETIME | AUTO | Creation timestamp |
| updated_at | DATETIME | AUTO_UPDATE | Last update timestamp |

**Indexes:**
- PRIMARY KEY (id)
- INDEX (vendor_id)
- INDEX (is_active)

**Constraints:**
- ON DELETE CASCADE (if vendor deleted, stores deleted)

---

### 7. product_product
**Purpose:** Products for sale

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO_INCREMENT | Product ID |
| store_id | INTEGER | FK(product_store.id), NULL | Store reference |
| category_id | INTEGER | FK(product_category.id), NULL | Category reference |
| name | VARCHAR(255) | NOT NULL | Product name |
| description | TEXT | NOT NULL | Product description |
| price | DECIMAL(10,2) | NOT NULL | Price in Rands |
| stock | INTEGER | DEFAULT 0 | Available quantity |
| image | VARCHAR(100) | NULL | Image file path |
| is_active | BOOLEAN | DEFAULT TRUE | Product status |
| created_at | DATETIME | AUTO | Creation timestamp |
| updated_at | DATETIME | AUTO_UPDATE | Last update timestamp |

**Indexes:**
- PRIMARY KEY (id)
- INDEX (store_id)
- INDEX (category_id)
- INDEX (is_active)
- INDEX (price)

**Constraints:**
- ON DELETE CASCADE (if store deleted, products deleted)
- ON DELETE SET NULL (if category deleted, product keeps NULL)

**Stock Rules:**
- 0 = Out of Stock (red)
- 1-10 = In Store Only (orange)
- 11+ = In Stock (green)

---

### 8. product_order
**Purpose:** Customer orders

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO_INCREMENT | Order ID |
| buyer_id | INTEGER | FK(auth_user.id) | Buyer reference |
| total_amount | DECIMAL(10,2) | NOT NULL | Total order cost |
| status | VARCHAR(20) | NOT NULL | Order status |
| order_date | DATETIME | AUTO | Order timestamp |

**Indexes:**
- PRIMARY KEY (id)
- INDEX (buyer_id)
- INDEX (order_date)
- INDEX (status)

**Status Values:**
- pending
- paid
- shipped
- delivered
- cancelled

**Constraints:**
- ON DELETE CASCADE (if buyer deleted, orders remain)

---

### 9. product_orderitem
**Purpose:** Individual items in orders

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO_INCREMENT | Item ID |
| order_id | INTEGER | FK(product_order.id) | Order reference |
| product_id | INTEGER | FK(product_product.id) | Product reference |
| quantity | INTEGER | NOT NULL | Quantity ordered |
| price | DECIMAL(10,2) | NOT NULL | Price at purchase |

**Indexes:**
- PRIMARY KEY (id)
- INDEX (order_id)
- INDEX (product_id)

**Constraints:**
- ON DELETE CASCADE (if order deleted, items deleted)
- ON DELETE PROTECT (cannot delete product in orders)

**Note:** Price stored at purchase time (preserves history even if product price changes)

---

### 10. product_review
**Purpose:** Product reviews by buyers

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTO_INCREMENT | Review ID |
| product_id | INTEGER | FK(product_product.id) | Product reference |
| user_id | INTEGER | FK(auth_user.id) | Reviewer reference |
| rating | INTEGER | NOT NULL | Star rating (1-5) |
| comment | TEXT | NOT NULL | Review comment |
| verified | BOOLEAN | DEFAULT FALSE | Purchase verification |
| created_at | DATETIME | AUTO | Review timestamp |

**Indexes:**
- PRIMARY KEY (id)
- INDEX (product_id)
- INDEX (user_id)
- INDEX (verified)
- UNIQUE (product_id, user_id) - One review per user per product

**Constraints:**
- ON DELETE CASCADE (if product deleted, reviews deleted)
- ON DELETE CASCADE (if user deleted, reviews deleted)

**Verification Logic:**
- Auto-set on save by checking OrderItem table
- If user has purchased product → verified = TRUE
- Otherwise → verified = FALSE

---

## Relationships Diagram (Text)

```
auth_user (Users)
├── 1:N → auth_user_groups (Group membership)
├── 1:N → accounts_resettoken (Password reset)
├── 1:N → product_store (Vendor's stores)
├── 1:N → product_order (Buyer's orders)
└── 1:N → product_review (User's reviews)

product_category (Categories)
└── 1:N → product_product (Products in category)

product_store (Stores)
└── 1:N → product_product (Products in store)

product_product (Products)
├── 1:N → product_orderitem (Product in orders)
└── 1:N → product_review (Reviews for product)

product_order (Orders)
└── 1:N → product_orderitem (Items in order)
```

---

## Data Integrity Rules

### Cascading Deletes
**When Store deleted:**
- All products in store → DELETED
- All order items remain (PROTECT constraint)

**When Product deleted:**
- Reviews for product → DELETED
- Order items → PROTECTED (cannot delete product in orders)

**When User deleted:**
- Stores owned → DELETED
- Products → DELETED (via store cascade)
- Orders → REMAIN (historical data)
- Reviews → DELETED

### Unique Constraints
- Username (unique across users)
- Email (unique across users)
- Store name per vendor (not enforced, but recommended)
- Review per user per product (UNIQUE constraint)
- Reset token (unique)

### Foreign Key Constraints
- All FK relationships enforced at database level
- Referential integrity maintained
- Invalid FK values rejected

---

## Session Storage

**Django Session Table:** django_session

| Column | Type | Description |
|--------|------|-------------|
| session_key | VARCHAR(40) | PK, Session ID |
| session_data | TEXT | Encoded session data |
| expire_date | DATETIME | Expiration timestamp |

**Session Data Contains:**
- User ID (authentication)
- Shopping cart (product_id: quantity pairs)
- CSRF tokens
- Flash messages

**Session Cleanup:**
- Expired sessions deleted automatically
- Manual cleanup: `python manage.py clearsessions`

---

## Indexes Strategy

### Performance Optimization
**Heavy Read Tables:**
- product_product: Indexed on (is_active, price, category_id)
- product_order: Indexed on (buyer_id, order_date)
- product_review: Indexed on (product_id, verified)

**Join Optimization:**
- Foreign keys automatically indexed
- Composite indexes for common queries

### Query Patterns
**Common Queries:**
1. Active products: `WHERE is_active = TRUE`
2. Products by category: `WHERE category_id = X AND is_active = TRUE`
3. Vendor's stores: `WHERE vendor_id = X`
4. Buyer's orders: `WHERE buyer_id = X ORDER BY order_date DESC`
5. Product reviews: `WHERE product_id = X ORDER BY verified DESC, created_at DESC`

---

## Data Migration Plan

### From SQLite to MariaDB
**Completed Steps:**
1. ✓ Install MariaDB 10.6
2. ✓ Create database `ecommerce_db`
3. ✓ Create user `ecommerce_user`
4. ✓ Update Django settings
5. ✓ Run migrations
6. ✓ Create superuser

**Fresh Database:**
- MariaDB database starts empty
- All data in SQLite `db.sqlite3` (old)
- No data migration performed (clean start acceptable for capstone)

**Future: Data Migration (if needed)**
```bash
# Export from SQLite
python manage.py dumpdata > data.json

# Import to MariaDB
python manage.py loaddata data.json
```

---

## Database Maintenance

### Backups (Production)
**Frequency:** Daily at 2 AM
**Retention:** 30 days
**Method:** `mysqldump` automated script
**Storage:** Separate server or cloud storage

### Monitoring
**Key Metrics:**
- Connection count
- Query performance
- Disk space usage
- Table sizes
- Index usage

### Optimization
**Regular Tasks:**
- Analyze tables monthly
- Optimize tables quarterly
- Review slow queries
- Update statistics

---

## Database Configuration

### MariaDB Settings (Production)
```ini
max_connections = 100
innodb_buffer_pool_size = 256M
query_cache_size = 64M
tmp_table_size = 64M
max_allowed_packet = 64M
```

### Django Database Settings
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'USER': 'ecommerce_user',
        'PASSWORD': 'ecommerce_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

---

## Estimated Data Sizes

### Assumptions (1 Year Operation)
- 100 users (50 vendors, 50 buyers)
- 200 stores (2 per vendor avg)
- 1,000 products (5 per store avg)
- 500 orders (10 per buyer avg)
- 2,000 order items (4 per order avg)
- 500 reviews (50% of orders)

### Storage Estimates
- Users: ~10 KB
- Stores: ~50 KB
- Products: ~500 KB
- Orders: ~100 KB
- Order Items: ~200 KB
- Reviews: ~100 KB
- Product Images: ~50 MB
- **Total Database:** ~1 MB
- **Total with Media:** ~51 MB

**Scalable to:** 10,000 users, 100,000 products with minimal changes
