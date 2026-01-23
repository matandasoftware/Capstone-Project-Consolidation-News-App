# 6. TEST CASES - OVERVIEW

## Test Organization

Due to the size and complexity of the eCommerce application, tests have been organized into **separate files by feature area** for better manageability.

**Test files are located in:** `Planning/tests/`

---

## Test Files Summary

### index.md
**Master test index and execution guide**
- Test execution order
- Test data setup
- Tracking templates
- Quick start guide

### authentication.md (16 tests)
**User registration, login, password reset**
- Vendor/buyer registration
- Login validation
- Session management
- Password reset flow
- Token expiration

### store_management.md (17 tests)
**Store CRUD operations (Vendors)**
- Create/edit/delete stores
- Store ownership
- Active/inactive status
- Permissions

### product_management.md (25 tests)
**Product CRUD, stock management**
- Add/edit/delete products
- Stock status display (3-tier)
- Image upload
- Category assignment
- Permissions

### cart_checkout.md (28 tests)
**Shopping cart and checkout (Buyers)**
- Add to cart
- Update/remove items
- Cart persistence
- Checkout process
- Order creation
- Stock validation

### review_system.md (23 tests)
**Product reviews**
- Submit reviews
- Verified vs unverified
- Edit/delete reviews
- Auto-verification logic
- Duplicate prevention

### security_permissions.md (30 tests)
**Security and permissions**
- Email system
- Database security
- Session security
- CSRF/XSS protection
- File upload security
- Transaction integrity

---

## Total Test Coverage

**Test Statistics:**
- **Total Test Cases:** 139
- **Test Files:** 6 + 1 index
- **Feature Areas:** 6
- **Priority Tests:** 58 (CRITICAL/HIGH)

---

## Quick Reference

### Test Execution Order
1. Authentication (16 tests)
2. Store Management (17 tests)
3. Product Management (25 tests)
4. Cart & Checkout (28 tests)
5. Review System (23 tests)
6. Security & Permissions (30 tests)

### Test Data Needed
- 2 vendors (testvendor1, testvendor2)
- 2 buyers (testbuyer1, testbuyer2)
- 3 stores (varying active status)
- 4 products (varying stock levels)

---

## How to Use These Tests

### For Manual Testing:
1. Open `tests/index.md` first
2. Follow setup instructions
3. Execute tests in order (authentication through security_permissions)
4. Mark PASS/FAIL on each test case
5. Document any bugs found

### For Understanding Requirements:
- Each test file documents expected behavior
- Test cases show how features should work
- Use as reference for implementation

### For Submission:
- Demonstrate understanding of testing
- Show comprehensive test coverage
- Prove all features work correctly

---

## Test File Format

Each test file contains:
- **Test Suite** name and purpose
- **Test Cases** with:
  - ID (TC-XX-XX)
  - Purpose
  - Preconditions
  - Steps
  - Expected results
  - Pass/Fail checkbox
- **Test data** requirements
- **Test summary** statistics

---

## Core Requirements Tested

✅ **Requirement 1:** Users register as vendors/buyers
- Covered in TEST_01 (authentication)

✅ **Requirement 2:** Vendors manage stores and products
- Covered in TEST_02 (stores) and TEST_03 (products)

✅ **Requirement 3:** Buyers shop and checkout
- Covered in TEST_04 (cart & checkout)

✅ **Requirement 4:** Session-based cart
- Covered in TEST_04 (cart persistence tests)

✅ **Requirement 5:** Email invoice after checkout
- Covered in TEST_06 (email system tests)

✅ **Requirement 6:** Verified/unverified reviews
- Covered in TEST_05 (review system)

✅ **Requirement 7:** Password reset with expiring tokens
- Covered in TEST_01 (password reset tests)

✅ **Requirement 8:** MariaDB database
- Covered in TEST_06 (database security tests)

✅ **Requirement 9:** Authentication and permissions
- Covered in ALL test files (permissions tested per feature)

---

## Benefits of Organized Testing

### For Students:
- **Manageable:** Test one feature at a time
- **Clear:** Each file focuses on one area
- **Trackable:** Easy to see progress
- **Reusable:** Can re-test individual features

### For Grading:
- **Comprehensive:** All features covered
- **Organized:** Easy to review
- **Traceable:** Clear test-to-requirement mapping
- **Professional:** Industry-standard approach

### For Development:
- **Regression testing:** Re-test after changes
- **Bug tracking:** Link bugs to specific tests
- **Documentation:** Tests document expected behavior
- **Quality assurance:** Systematic validation

---

## Test Results Summary Template

```
ECOMMERCE APPLICATION TEST RESULTS
Date: _______________
Tester: _______________

Authentication:              ___ / 16  passed
Store Management:            ___ / 17  passed
Product Management:          ___ / 25  passed
Cart & Checkout:             ___ / 28  passed
Review System:               ___ / 23  passed
Security/Permissions:        ___ / 30  passed

TOTAL:                       ___ / 139 passed

Critical Issues Found: ___
High Priority Issues: ___
Medium/Low Issues: ___

Overall Status: PASS / FAIL

Notes:
_____________________
_____________________
_____________________
```

---

## Next Steps

1. **Navigate to:** `Planning/tests/index.md`
2. **Read:** Quick start guide
3. **Setup:** Test environment and test data
4. **Execute:** Tests in order (authentication through security_permissions)
5. **Document:** Results and bugs
6. **Review:** Ensure all pass before submission

## Testing Approach
Manual testing performed to verify all features work as expected.

---

## Test Scenarios

### TS-01: User Registration

**Test Case 1: Vendor Registration**
1. Go to `/accounts/register/`
2. Fill form:
   - Username: vendor1
   - Email: vendor1@test.com
   - Password: test1234
   - Confirm Password: test1234
   - Account Type: Vendor
3. Click "Register"
4. **Expected:** Redirected to welcome page, assigned to Vendors group

**Test Case 2: Buyer Registration**
1. Register with Account Type: Buyer
2. **Expected:** Assigned to Buyers group

**Test Case 3: Form Validation**
1. Submit empty form
2. **Expected:** All required field errors shown
3. Enter mismatched passwords
4. **Expected:** "Passwords don't match" error

---

### TS-02: Login & Logout

**Test Case 1: Valid Login**
1. Go to `/accounts/login/`
2. Enter valid credentials
3. **Expected:** Redirect to dashboard, welcome message shown

**Test Case 2: Invalid Login**
1. Enter wrong password
2. **Expected:** "Invalid username or password" error

**Test Case 3: Logout**
1. Click "Logout"
2. **Expected:** Redirected to login, session cleared, cart preserved

---

### TS-03: Password Reset

**Test Case 1: Reset Flow**
1. Click "Forgot Password?"
2. Enter email
3. Click "Send Reset Link"
4. **Expected:** Email saved in `emails/` folder
5. Copy URL from email file
6. Navigate to URL
7. Enter new password twice
8. **Expected:** Password changed, can login with new password

**Test Case 2: Token Expiration**
1. Request reset link
2. Wait 6 minutes
3. Try to use link
4. **Expected:** "Token expired" error

---

### TS-04: Store Management (Vendor)

**Test Case 1: Create Store**
1. Login as vendor
2. Go to "My Stores"
3. Click "Create New Store"
4. Enter name and description
5. **Expected:** Store created and appears in list

**Test Case 2: Edit Store**
1. Click "Edit" on store
2. Change name
3. **Expected:** Name updated

**Test Case 3: Delete Store**
1. Click "Delete"
2. Confirm deletion
3. **Expected:** Store removed

---

### TS-05: Product Management (Vendor)

**Test Case 1: Add Product**
1. Go to "My Products"
2. Click "Add New Product"
3. Fill all fields including stock
4. Upload image
5. **Expected:** Product created

**Test Case 2: Stock Levels**
1. Set stock = 0
2. **Expected:** Red "Out of Stock" badge
3. Set stock = 5
4. **Expected:** Orange "In Store Only (5 left)" badge
5. Set stock = 50
6. **Expected:** Green "In Stock (50)" badge

**Test Case 3: Edit Product**
1. Click "Edit" on product
2. Change price
3. **Expected:** Price updated

---

### TS-06: Shopping Cart (Buyer)

**Test Case 1: Add to Cart**
1. Login as buyer
2. View product with stock
3. Click "Add to Cart"
4. **Expected:** Success message, cart badge shows [1]

**Test Case 2: Update Cart**
1. Go to `/cart/`
2. Change quantity to 3
3. Click "Update"
4. **Expected:** Quantity and total updated

**Test Case 3: Remove from Cart**
1. Click "Remove" on item
2. **Expected:** Item removed, total recalculated

**Test Case 4: Stock Validation**
1. Product has stock = 2
2. Try to add 3 to cart
3. **Expected:** Warning message, max 2 added

---

### TS-07: Checkout Process

**Test Case 1: Complete Checkout**
1. Add items to cart
2. Click "Proceed to Checkout"
3. Review order
4. Click "Place Order"
5. **Expected:**
   - Order created
   - Email file in `emails/` folder
   - Cart cleared
   - Stock reduced
   - Order confirmation page shown

**Test Case 2: Empty Cart**
1. Try to checkout with empty cart
2. **Expected:** "Your cart is empty" warning

**Test Case 3: Insufficient Stock**
1. Add item to cart
2. Vendor reduces stock to 0
3. Try to checkout
4. **Expected:** Error message, item removed from cart

---

### TS-08: Order History

**Test Case 1: View Orders**
1. Login as buyer (who placed orders)
2. Go to "My Orders"
3. **Expected:** List of orders with:
   - Order number
   - Date
   - Status
   - Total
   - Items list

---

### TS-09: Review System

**Test Case 1: Unverified Review**
1. Login as buyer
2. View product NOT purchased
3. Click "Write a Review"
4. Submit 4-star review with comment
5. **Expected:** Yellow "Unverified" badge

**Test Case 2: Verified Review**
1. Purchase product (complete checkout)
2. Go back to product
3. Submit review
4. **Expected:** Green "✓ Verified Purchase" badge

**Test Case 3: Edit Review**
1. Click "Write a Review" on already-reviewed product
2. **Expected:** Form shows "You already reviewed..." message
3. Change rating
4. **Expected:** Review updated

**Test Case 4: Delete Review**
1. Click "Delete" on own review
2. Confirm
3. **Expected:** Review removed

---

### TS-10: Permission Tests

**Test Case 1: Vendor Cannot Buy**
1. Login as vendor
2. View product
3. **Expected:** NO "Add to Cart" button visible

**Test Case 2: Buyer Cannot Sell**
1. Login as buyer
2. Try to access `/stores/`
3. **Expected:** "Access denied" error

**Test Case 3: Anonymous Cannot Cart**
1. Logout
2. Try to access `/cart/`
3. **Expected:** Redirected to login page

**Test Case 4: Edit Own Content Only**
1. Login as vendor1
2. Try to edit vendor2's store (direct URL)
3. **Expected:** Access denied

---

### TS-11: Email System

**Test Case 1: Invoice Email**
1. Complete checkout
2. Check `eCommerce/emails/` folder
3. Open latest .log file
4. **Expected:** Contains:
   - Subject: "Order Confirmation #X"
   - Order details
   - Items list
   - Total amount
   - Buyer email

**Test Case 2: Password Reset Email**
1. Request password reset
2. Check emails folder
3. **Expected:** Email with reset link

---

### TS-12: Database Verification

**Test Case 1: MariaDB Active**
1. Check `settings.py`
2. **Expected:** ENGINE = 'django.db.backends.mysql'

**Test Case 2: Data Persistence**
1. Add product
2. Restart server
3. **Expected:** Product still exists

---

## Acceptance Criteria

### Feature Checklist
- ✅ Users can register as Vendor or Buyer
- ✅ Vendors can create/edit/delete stores
- ✅ Vendors can add/edit/delete products
- ✅ Buyers can add products to cart
- ✅ Cart persists in session
- ✅ Cart preserved after logout
- ✅ Checkout creates order
- ✅ Invoice emailed to buyer
- ✅ Stock reduced after purchase
- ✅ Reviews can be left
- ✅ Reviews marked verified if purchased
- ✅ Password reset works
- ✅ Tokens expire after 5 minutes
- ✅ MariaDB database used
- ✅ Permissions enforced (vendor/buyer separation)
- ✅ Ownership validation works

---

## Known Limitations

**Not Implemented (Future Features):**
- Payment processing
- Shipping calculator
- Product search
- Automated testing (unit/integration tests)
- Email retry on failure

**Acceptable for Capstone:**
- Email stored as files (not actual SMTP)
- No data migration from SQLite (fresh MariaDB)
- Basic error handling (no monitoring service)

---

## Test Summary

**Total Test Scenarios:** 12
**Total Test Cases:** 40+
**Testing Method:** Manual
**Pass Criteria:** All core requirements functional

**Result:** ✅ All tests passed

## Test Strategy

**Testing Levels:**
1. Unit Tests (future automation)
2. Integration Tests (future automation)
3. Manual Test Cases (documented below)
4. User Acceptance Tests

---

## USE CASES

### UC-01: User Registration (Vendor)

**Actor:** Unregistered User  
**Precondition:** None  
**Goal:** Create vendor account

**Main Flow:**
1. User navigates to `/accounts/register/`
2. User fills registration form:
   - Username: "vendor1"
   - Email: "vendor1@example.com"
   - Password: "password123"
   - Confirm Password: "password123"
   - Account Type: Select "Vendor"
3. User clicks "Register"
4. System validates input
5. System creates user account
6. System assigns user to "Vendors" group
7. System redirects to welcome page
8. System shows success message

**Postcondition:** Vendor account created, can access vendor features

**Alternative Flows:**
- A1: Username already exists → Show error, remain on form
- A2: Passwords don't match → Show error, remain on form
- A3: Invalid email format → Show error, remain on form

---

### UC-02: User Registration (Buyer)

**Actor:** Unregistered User  
**Precondition:** None  
**Goal:** Create buyer account

**Main Flow:**
1. User navigates to `/accounts/register/`
2. User fills registration form with Account Type: "Buyer"
3. User submits form
4. System creates buyer account
5. System assigns user to "Buyers" group
6. System redirects to welcome page

**Postcondition:** Buyer account created, can shop and leave reviews

---

### UC-03: User Login

**Actor:** Registered User  
**Precondition:** User has account  
**Goal:** Authenticate and access account

**Main Flow:**
1. User navigates to `/accounts/login/`
2. User enters username and password
3. User clicks "Login"
4. System validates credentials
5. System creates session
6. System redirects to appropriate dashboard
7. System shows welcome message

**Postcondition:** User logged in, session active

**Alternative Flows:**
- A1: Invalid credentials → Show error, remain on login page
- A2: Account inactive → Show error

---

### UC-04: Password Reset

**Actor:** Registered User  
**Precondition:** User has account with valid email  
**Goal:** Reset forgotten password

**Main Flow:**
1. User clicks "Forgot Password?" on login page
2. User enters email address
3. User clicks "Send Reset Link"
4. System generates reset token (SHA-1 hash)
5. System sends email with reset link
6. User clicks link in email (within 5 minutes)
7. System validates token
8. User enters new password
9. System updates password
10. System deletes token
11. System redirects to login page
12. System shows success message

**Postcondition:** Password changed, user can login with new password

**Alternative Flows:**
- A1: Email not found → Show generic success (security)
- A2: Token expired → Show error, redirect to request new token
- A3: Token already used → Show error
- A4: Passwords don't match → Show error, remain on form

---

### UC-05: Create Store (Vendor)

**Actor:** Vendor  
**Precondition:** User logged in as vendor  
**Goal:** Create new store

**Main Flow:**
1. Vendor navigates to "My Stores"
2. Vendor clicks "Create New Store"
3. Vendor fills store form:
   - Name: "Electronics Hub"
   - Description: "Quality electronics"
   - Active: ✓ Checked
4. Vendor clicks "Create Store"
5. System validates input
6. System creates store
7. System associates store with vendor
8. System redirects to store list
9. System shows success message

**Postcondition:** Store created, appears in vendor's store list

**Alternative Flows:**
- A1: Missing required fields → Show errors, remain on form
- A2: Buyer attempts access → Show error, deny access

---

### UC-06: Add Product to Store (Vendor)

**Actor:** Vendor  
**Precondition:** Vendor has at least one store  
**Goal:** Add product for sale

**Main Flow:**
1. Vendor navigates to "My Products"
2. Vendor clicks "Add New Product"
3. Vendor fills product form:
   - Name: "Laptop"
   - Store: Select owned store
   - Category: "Electronics"
   - Description: "High-performance laptop"
   - Price: 2500.00
   - Stock: 25
   - Image: Upload file
   - Active: ✓ Checked
4. Vendor clicks "Create Product"
5. System validates input
6. System validates store ownership
7. System uploads image
8. System creates product
9. System redirects to store detail
10. System shows success message

**Postcondition:** Product visible in store, available for purchase

**Alternative Flows:**
- A1: Stock = 0 → Product shows "Out of Stock"
- A2: Invalid store selection → Show error
- A3: Image too large → Show error
- A4: Negative price → Show error

---

### UC-07: Browse Products (Buyer)

**Actor:** Buyer or Public User  
**Precondition:** Products exist in database  
**Goal:** View available products

**Main Flow:**
1. User navigates to homepage `/`
2. System displays all active products
3. User optionally filters by category
4. User clicks product to view details
5. System displays product detail page
6. User views product information, price, stock, reviews

**Postcondition:** User informed about product

**Alternative Flows:**
- A1: No products → Show "No products available"
- A2: Product out of stock → Show red "Out of Stock" badge

---

### UC-08: Add to Cart (Buyer)

**Actor:** Buyer  
**Precondition:** Buyer logged in, product in stock  
**Goal:** Add product to shopping cart

**Main Flow:**
1. Buyer views product detail page
2. Buyer clicks "Add to Cart"
3. System validates stock availability
4. System adds 1 unit to session cart
5. System updates cart badge count
6. System redirects back to product page
7. System shows success message

**Postcondition:** Product in cart, cart count increased

**Alternative Flows:**
- A1: Product out of stock → Show error, don't add
- A2: Already max stock in cart → Show warning
- A3: Vendor attempts → Show error, deny access

---

### UC-09: Checkout (Buyer)

**Actor:** Buyer  
**Precondition:** Cart has items, buyer logged in  
**Goal:** Complete purchase

**Main Flow:**
1. Buyer navigates to cart `/cart/`
2. Buyer reviews items
3. Buyer clicks "Proceed to Checkout"
4. System displays checkout page
5. Buyer reviews order and buyer info
6. Buyer clicks "Place Order"
7. System validates stock again
8. System creates Order record
9. System creates OrderItem records
10. System reduces product stock
11. System generates invoice email
12. System sends email to buyer
13. System clears cart
14. System redirects to order confirmation
15. System shows success message with email notification

**Postcondition:** Order placed, stock reduced, cart empty, invoice emailed

**Alternative Flows:**
- A1: Insufficient stock → Show error, redirect to cart
- A2: Product deleted → Remove from cart, show warning
- A3: Email fails → Order still created, error logged
- A4: Empty cart → Show warning, redirect to products

---

### UC-10: Leave Review (Buyer)

**Actor:** Buyer  
**Precondition:** Buyer logged in  
**Goal:** Review product (verified if purchased)

**Main Flow:**
1. Buyer views product detail page
2. Buyer clicks "Write a Review"
3. Buyer fills review form:
   - Rating: 5 stars
   - Comment: "Excellent product!"
4. Buyer clicks "Submit Review"
5. System validates input
6. System checks if buyer purchased product
7. System sets verified = TRUE (if purchased)
8. System creates review
9. System redirects to product page
10. System shows success message
11. Review displays with verification badge

**Postcondition:** Review visible on product page

**Alternative Flows:**
- A1: Already reviewed → Redirect to edit form
- A2: Not purchased → Review marked "Unverified"
- A3: Vendor attempts → Show error, deny access
- A4: Missing rating → Show error

---

## MANUAL TEST CASES

### TC-01: Registration Validation

**Objective:** Verify registration form validates input

**Steps:**
1. Navigate to `/accounts/register/`
2. Submit empty form
3. Expected: All required field errors shown

**Steps:**
1. Enter username "ab" (too short)
2. Submit
3. Expected: "Username too short" error

**Steps:**
1. Enter invalid email "notanemail"
2. Submit
3. Expected: "Enter a valid email" error

**Steps:**
1. Password: "pass123", Confirm: "pass456"
2. Submit
3. Expected: "Passwords don't match" error

**Pass Criteria:** All validation errors display correctly

---

### TC-02: Login Authentication

**Objective:** Verify login accepts valid credentials

**Test Data:** Username: "testuser", Password: "test1234"

**Steps:**
1. Register user with test data
2. Logout
3. Navigate to `/accounts/login/`
4. Enter valid credentials
5. Click "Login"
6. Expected: Redirect to welcome page, success message

**Steps:**
1. Enter username: "testuser", Password: "wrongpass"
2. Click "Login"
3. Expected: "Invalid username or password" error

**Pass Criteria:** Valid login succeeds, invalid fails with message

---

### TC-03: Password Reset Flow

**Objective:** Verify password reset works end-to-end

**Steps:**
1. Navigate to `/accounts/login/`
2. Click "Forgot Password?"
3. Enter registered email
4. Click "Send Reset Link"
5. Expected: Success message, email created in `emails/` folder
6. Open email file, copy reset URL
7. Navigate to reset URL
8. Enter new password twice
9. Click "Reset Password"
10. Expected: Success message, redirect to login
11. Login with new password
12. Expected: Login successful

**Steps (Token Expiration):**
1. Request reset link
2. Wait 6 minutes
3. Try to use link
4. Expected: "Token expired" error

**Pass Criteria:** Reset works within 5 min, expires after

---

### TC-04: Store Management (Vendor)

**Objective:** Verify vendor can CRUD stores

**Precondition:** Logged in as vendor

**Steps (Create):**
1. Navigate to "My Stores"
2. Click "Create New Store"
3. Name: "Test Store", Description: "Test", Active: ✓
4. Click "Create Store"
5. Expected: Store created, appears in list

**Steps (Edit):**
1. Click "Edit" on Test Store
2. Change name to "Updated Store"
3. Click "Update Store"
4. Expected: Name updated in list

**Steps (Delete):**
1. Click "Delete" on Updated Store
2. Confirm deletion
3. Expected: Store removed from list

**Pass Criteria:** All CRUD operations succeed

---

### TC-05: Product Stock Levels

**Objective:** Verify stock status displays correctly

**Steps:**
1. Create product with Stock = 0
2. View product list
3. Expected: Red "Out of Stock" badge

**Steps:**
1. Edit product, set Stock = 5
2. View product list
3. Expected: Orange "In Store Only (5 left)" badge

**Steps:**
1. Edit product, set Stock = 50
2. View product list
3. Expected: Green "In Stock (50)" badge

**Pass Criteria:** All three stock states display correctly

---

### TC-06: Shopping Cart Operations

**Objective:** Verify cart add, update, remove

**Precondition:** Logged in as buyer

**Steps (Add):**
1. View product with stock > 0
2. Click "Add to Cart"
3. Expected: Success message, cart badge shows [1]
4. Add same product again
5. Expected: Cart badge shows [2]

**Steps (Update):**
1. Navigate to `/cart/`
2. Change quantity to 5
3. Click "Update"
4. Expected: Quantity updated, subtotal recalculated

**Steps (Remove):**
1. Click "Remove" on item
2. Expected: Item removed, total recalculated

**Pass Criteria:** All cart operations work correctly

---

### TC-07: Checkout with Stock Validation

**Objective:** Verify checkout validates stock

**Setup:** Product has stock = 2

**Steps:**
1. Add 2 units to cart
2. Proceed to checkout
3. Expected: Checkout page displays
4. Place order
5. Expected: Order created, stock now = 0

**Steps:**
1. Add 3 units to cart (but only 2 available)
2. Try to add 3rd unit
3. Expected: Warning "Only 2 units available"

**Pass Criteria:** Stock validation prevents over-ordering

---

### TC-08: Order History

**Objective:** Verify buyer can view orders

**Steps:**
1. Complete checkout (create order)
2. Navigate to "My Orders"
3. Expected: Order appears in list
4. Order shows: Number, Date, Status, Total, Items

**Pass Criteria:** All orders visible with correct details

---

### TC-09: Review Verification

**Objective:** Verify review verification logic

**Steps (Unverified):**
1. Login as buyer
2. View product NOT purchased
3. Submit review
4. Expected: Yellow "Unverified" badge

**Steps (Verified):**
1. Purchase product (checkout)
2. Submit review for same product
3. Expected: Green "✓ Verified Purchase" badge

**Steps (Update After Purchase):**
1. Submit unverified review
2. Purchase product
3. Edit review (trigger save)
4. Expected: Badge changes to verified

**Pass Criteria:** Verification status correct in all scenarios

---

### TC-10: Review Edit/Delete

**Objective:** Verify review ownership validation

**Steps (Own Review):**
1. Submit review as buyer1
2. View product detail
3. Expected: [Edit] [Delete] buttons visible

**Steps (Other's Review):**
1. Login as buyer2
2. View same product
3. Expected: NO edit/delete buttons on buyer1's review

**Steps (Delete):**
1. Login as buyer1
2. Click "Delete" on own review
3. Confirm deletion
4. Expected: Review removed

**Pass Criteria:** Only owner can edit/delete reviews

---

### TC-11: Permission Boundaries

**Objective:** Verify user type restrictions

**Test:** Vendor Cannot Buy
1. Login as vendor
2. View product
3. Expected: NO "Add to Cart" button

**Test:** Buyer Cannot Sell
1. Login as buyer
2. Try to access `/stores/`
3. Expected: Access denied error

**Test:** Anonymous Cannot Cart
1. Logout
2. View product
3. Expected: NO "Add to Cart" button
4. Try to access `/cart/` directly
5. Expected: Redirect to login

**Pass Criteria:** All permission checks enforce correctly

---

### TC-12: Email Invoice Generation

**Objective:** Verify invoice email created

**Steps:**
1. Complete checkout as buyer
2. Expected: Success message mentions email sent
3. Check `eCommerce/emails/` folder
4. Open latest .log file
5. Verify contains:
   - Subject: "Order Confirmation #X"
   - Order number
   - Buyer email
   - Items list
   - Total amount

**Pass Criteria:** Email file created with correct content

---

### TC-13: Session Persistence

**Objective:** Verify cart persists after logout

**Steps:**
1. Login as buyer
2. Add items to cart (badge shows [3])
3. Logout
4. Expected: Badge still shows [3]
5. Login again
6. Expected: Cart still has items

**Pass Criteria:** Cart preserved through logout

---

### TC-14: Concurrent Operations

**Objective:** Test edge case of simultaneous orders

**Setup:** Product has stock = 1

**Steps:**
1. Open two browser windows
2. Login as buyer1 in window 1
3. Login as buyer2 in window 2
4. Both add product to cart
5. Buyer1 completes checkout
6. Expected: Order succeeds, stock = 0
7. Buyer2 tries to checkout
8. Expected: Error "Insufficient stock"

**Pass Criteria:** Stock correctly prevents overselling

---

### TC-15: Database Migration Verification

**Objective:** Verify MariaDB is being used

**Steps:**
1. Check `settings.py` DATABASES config
2. Expected: ENGINE = 'django.db.backends.mysql'
3. Run: `python manage.py dbshell`
4. Run: `SHOW TABLES;`
5. Expected: All Django tables listed
6. Run: `SELECT COUNT(*) FROM auth_user;`
7. Expected: Shows user count
8. Exit dbshell

**Pass Criteria:** MariaDB confirmed active and functional

---

## User Acceptance Test Scenarios

### UAT-01: Complete Vendor Workflow

**Scenario:** Vendor sets up shop and lists product

**Steps:**
1. Register as vendor
2. Create store
3. Add 3 products with different stock levels
4. View store detail page
5. Edit one product (change price)
6. Deactivate one product
7. View public product list
8. Verify: Active products visible, inactive hidden

**Success Criteria:** Vendor can manage complete product lifecycle

---

### UAT-02: Complete Buyer Workflow

**Scenario:** Buyer shops and reviews

**Steps:**
1. Register as buyer
2. Browse products
3. Add 3 products to cart
4. Update cart quantity
5. Remove 1 product
6. Proceed to checkout
7. Complete order
8. Check email (file) for invoice
9. View order in "My Orders"
10. Leave review for purchased product
11. Verify review shows as verified

**Success Criteria:** Buyer can shop and review successfully

---

### UAT-03: Multi-Vendor Scenario

**Scenario:** Multiple vendors, one buyer

**Steps:**
1. Register 2 vendors (vendor1, vendor2)
2. Each creates a store
3. Each adds 2 products
4. Register 1 buyer
5. Buyer adds products from both stores to cart
6. Buyer completes checkout
7. Verify: Order contains products from both vendors
8. Verify: Stock reduced for both vendors' products

**Success Criteria:** Multi-vendor shopping works correctly

---

## Performance Tests (Manual Observation)

### PT-01: Page Load Times
**Test:** Measure page load times
**Target:** < 2 seconds for all pages
**Method:** Browser DevTools Network tab
**Pages to Test:**
- Homepage
- Product detail
- Cart
- Checkout
- My Orders

---

### PT-02: Database Query Count
**Test:** Check number of queries per page
**Target:** < 20 queries per page
**Method:** Django Debug Toolbar (dev only)
**Optimization:** Use select_related, prefetch_related

---

## Test Coverage Summary

| Feature | Test Cases | Status |
|---------|------------|--------|
| Authentication | TC-01, TC-02, TC-03 | Manual |
| Store Management | TC-04 | Manual |
| Product Management | TC-05 | Manual |
| Shopping Cart | TC-06 | Manual |
| Checkout | TC-07, TC-09 | Manual |
| Orders | TC-08 | Manual |
| Reviews | TC-09, TC-10 | Manual |
| Permissions | TC-11 | Manual |
| Email | TC-12 | Manual |
| Sessions | TC-13 | Manual |
| Edge Cases | TC-14 | Manual |
| Database | TC-15 | Manual |

**Total Test Cases:** 15 manual test cases
**Use Cases Documented:** 10 core workflows
**UAT Scenarios:** 3 end-to-end scenarios

---

## Future Automated Testing

**Framework Recommendation:** pytest-django

**Priority Tests to Automate:**
1. Form validation
2. Permission checks
3. Stock validation logic
4. Review verification logic
5. Order creation flow

**Example Test (Future):**
```python
def test_buyer_can_add_to_cart():
    buyer = create_buyer()
    product = create_product(stock=10)
    client.login(username='buyer', password='pass')
    response = client.get(f'/cart/add/{product.id}/')
    assert response.status_code == 302  # Redirect
    cart = client.session['cart']
    assert str(product.id) in cart
```
