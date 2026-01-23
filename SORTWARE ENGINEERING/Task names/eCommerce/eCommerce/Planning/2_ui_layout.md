# 2. UI LAYOUT PLAN

## Design Approach

**Framework:** Bootstrap 5 (responsive, mobile-friendly)

**Color Scheme:**
- Primary Blue: #0d6efd (buttons, links)
- Success Green: #198754 (in stock, success messages)
- Warning Orange: #fd7e14 (low stock)
- Danger Red: #dc3545 (out of stock, errors)
- Secondary Gray: #6c757d (inactive items)

---

## Navigation Structure

### All Pages Have:
**Navigation Bar (Top):**
- Logo/site name (clickable, goes to homepage)
- Main links: Products, Categories
- User-specific links:
  - **Buyers:** Cart (with item count badge), My Orders
  - **Vendors:** My Stores, My Products
- Right side: Username, Logout (or Login/Register if not logged in)

**Footer (Bottom):**
- Copyright notice

---

## Key Pages

### 1. Homepage (Product List)
**Purpose:** Browse all available products

**Layout:**
- Category filter buttons at top (All, Electronics, Clothing, etc.)
- Product grid: 3 columns on desktop, 2 on tablet, 1 on mobile
- Each product card shows:
  - Product image (or placeholder if no image)
  - Product name
  - Price in Rands (R)
  - Stock badge (colored: green/orange/red)
  - "View Details" button
  - "Add to Cart" button (buyers only, if in stock)

---

### 2. Product Detail Page
**Purpose:** View full product information

**Layout: Two columns**
- **Left:** Large product image
- **Right:** Product details
  - Name
  - Store name (clickable link)
  - Category
  - Price
  - Stock status with colored badge
  - Description
  - "Add to Cart" button (buyers only)

**Below:** Reviews section
- "Write a Review" button (buyers only)
- List of existing reviews with:
  - Username
  - Verified/Unverified badge
  - Star rating (1-5)
  - Date posted
  - Comment text
  - Edit/Delete buttons (for review owner only)

---

### 3. Shopping Cart (Buyers)
**Purpose:** Review items before checkout

**Layout: Two columns**
- **Left (Main):** Cart items list
  - Each item shows:
    - Product image (small)
    - Product name
    - Store name
    - Price per unit
    - Quantity selector
    - "Update" button
    - Subtotal
    - "Remove" button

- **Right (Sidebar):** Order summary
  - Item count
  - Total amount (large, prominent)
  - "Proceed to Checkout" button (green, large)
  - "Continue Shopping" link

**Empty cart:** Message with link to browse products

---

### 4. Checkout Page (Buyers)
**Purpose:** Confirm order before purchase

**Layout: Two columns**
- **Left:** Order review
  - List of items with quantities and prices
  - Buyer information (name, email)
  - Note: "Invoice will be emailed"

- **Right:** Order total
  - Item count
  - Total amount (prominent)
  - "Place Order" button (green, large)
  - "Back to Cart" link

---

### 5. My Stores (Vendors)
**Purpose:** Manage vendor's stores

**Layout:**
- "Create New Store" button (top right, prominent)
- List of stores as cards:
  - Store name
  - Description
  - Active/Inactive badge (green/gray)
  - Product count
  - Creation date
  - Action buttons: View Store, Edit, Delete

---

### 6. My Products (Vendors)
**Purpose:** Manage all products across stores

**Layout:**
- "Add New Product" button (top right)
- Table view with columns:
  - Image thumbnail
  - Product name
  - Store name
  - Category
  - Price
  - Stock (with colored badge)
  - Active/Inactive status
  - Actions: Edit, Delete

---

### 7. My Orders (Buyers)
**Purpose:** View order history

**Layout:**
- List of orders (newest first)
- Each order card shows:
  - Order number
  - Order date
  - Status badge (colored by status)
  - Total amount
  - Expandable item list with quantities

---

## Forms Design

**Standard Form Layout:**
- Field label with red asterisk (*) for required fields
- Full-width input fields
- Help text in gray below field (if needed)
- Error messages in red below field
- Primary button (blue) for submit
- Secondary button (gray) for cancel

**Key Forms:**
- Registration (username, email, password, account type)
- Login (username, password)
- Store form (name, description, active checkbox)
- Product form (all fields including image upload)
- Review form (rating dropdown, comment textarea)

---

## Status Badges

**Stock Status:**
- Out of Stock (0 items): Red badge
- In Store Only (1-10 items): Orange badge with count
- In Stock (11+ items): Green badge with count

**Review Verification:**
- Verified Purchase: Green badge with checkmark
- Unverified: Yellow/orange badge

**Store/Product Active Status:**
- Active: Green badge
- Inactive: Gray badge

**Order Status:**
- Pending: Yellow/orange badge
- Paid: Blue badge
- Shipped: Purple badge
- Delivered: Green badge
- Cancelled: Red badge

---

## User Feedback Messages

**Message Types (displayed at top of page):**
- **Success:** Green alert box with checkmark
  - Example: "Product added to cart!"
- **Error:** Red alert box
  - Example: "Invalid username or password"
- **Warning:** Yellow/orange alert box
  - Example: "Only 5 units available"
- **Info:** Blue alert box
  - Example: "Invoice sent to your email"

---

## Responsive Behavior

**Breakpoints:**
- Mobile: < 768px (single column, stacked layout)
- Tablet: 768-991px (2 columns for product grid)
- Desktop: ≥ 992px (3 columns for product grid)

**Mobile Optimizations:**
- Navigation collapses to hamburger menu
- Form fields stack vertically
- Buttons become full-width
- Tables become responsive/scrollable
- Touch-friendly button sizes (minimum 44px)

---

## Accessibility Features

- Semantic HTML (header, nav, main, footer, article, section)
- Alt text on all product images
- Form labels properly associated with inputs
- Keyboard navigation support
- Sufficient color contrast (WCAG AA standard)
- Focus indicators visible on interactive elements

---

## Confirmation Dialogs

**Delete Actions:**
- Separate confirmation page (not popup)
- Shows item being deleted
- Warning message (red)
- "Confirm Delete" button (red)
- "Cancel" button (gray)
- Note if action cannot be undone

---

## Key UI Features Implemented

✅ Bootstrap 5 responsive grid system
✅ Color-coded status badges
✅ Cart item count in navigation badge
✅ User role-specific navigation (vendor/buyer)
✅ Success/error/warning message system
✅ Image placeholders for products without photos
✅ Star rating visualization in reviews
✅ Verification badges for reviews
✅ Responsive design for all screen sizes
✅ Consistent button styling and placement
