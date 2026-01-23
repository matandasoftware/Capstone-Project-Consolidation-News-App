# TEST 06: PERMISSIONS & SECURITY

## Test Suite: Email System

### TC-06-01: Invoice Email - File Created
**Purpose:** Verify invoice email generated after checkout

**Steps:**
1. Complete checkout as buyer
2. Check `eCommerce/emails/` folder
3. Find latest .log file
4. Open and review contents

**Expected Result:**
- ✓ Email file exists
- ✓ Subject: "Order Confirmation #X - eCommerce Store"
- ✓ Contains order number
- ✓ Contains buyer email
- ✓ Contains itemized list
- ✓ Contains total amount
- ✓ HTML formatted

**Pass/Fail:** _______

---

### TC-06-02: Password Reset Email - File Created
**Purpose:** Verify reset email generated

**Steps:**
1. Request password reset
2. Check emails folder
3. Open file

**Expected Result:**
- ✓ Email file created
- ✓ Contains reset URL
- ✓ URL includes token
- ✓ Instructions included

**Pass/Fail:** _______

---

### TC-06-03: Email Success Message
**Purpose:** Verify user notified of email

**Steps:**
1. Complete checkout

**Expected Result:**
- ✓ Success message includes: "Invoice sent to [email]"
- ✓ User informed

**Pass/Fail:** _______

---

## Test Suite: Database Security

### TC-06-04: MariaDB Connection Active
**Purpose:** Verify using MariaDB not SQLite

**Steps:**
1. Check `settings.py`
2. Verify ENGINE = 'django.db.backends.mysql'
3. Run: `python manage.py dbshell`
4. Run: `SHOW TABLES;`

**Expected Result:**
- ✓ MariaDB shell opens
- ✓ All Django tables listed
- ✓ Data persists in MariaDB

**Pass/Fail:** _______

---

### TC-06-05: Password Hashing
**Purpose:** Verify passwords not stored in plaintext

**Steps:**
1. Create user account
2. Check database (admin panel or dbshell)
3. SELECT password FROM auth_user

**Expected Result:**
- ✓ Password field shows hash (e.g., "pbkdf2_sha256$...")
- ✓ NOT plaintext
- ✓ Cannot reverse to original

**Pass/Fail:** _______

---

### TC-06-06: SQL Injection Prevention
**Purpose:** Verify Django ORM protects against SQL injection

**Steps:**
1. Try to login with username: `admin' OR '1'='1`
2. Try product search with: `'; DROP TABLE products; --`

**Expected Result:**
- ✓ Treated as literal strings
- ✓ No SQL executed
- ✓ Django ORM parameterizes queries

**Pass/Fail:** _______

---

## Test Suite: Session Security

### TC-06-07: Session Cookie HTTP-Only
**Purpose:** Verify JavaScript cannot access session

**Steps:**
1. Login
2. Open browser console
3. Try: `document.cookie`

**Expected Result:**
- ✓ Session cookie NOT visible in JavaScript
- ✓ HTTP-only flag set
- ✓ Prevents XSS attacks

**Pass/Fail:** _______

---

### TC-06-08: Cart Stored in Session
**Purpose:** Verify cart in server-side session

**Steps:**
1. Add items to cart
2. Check browser localStorage/cookies

**Expected Result:**
- ✓ Cart NOT in localStorage
- ✓ Only session ID in cookie
- ✓ Cart data on server
- ✓ More secure

**Pass/Fail:** _______

---

### TC-06-09: Session Timeout
**Purpose:** Verify session expires after 10 minutes

**Steps:**
1. Login
2. Wait 11 minutes (no activity)
3. Try to access protected page

**Expected Result:**
- ✓ Session expired
- ✓ Redirected to login
- ✓ Must re-authenticate

**Pass/Fail:** _______

---

## Test Suite: CSRF Protection

### TC-06-10: CSRF Token in Forms
**Purpose:** Verify all forms have CSRF protection

**Steps:**
1. View page source of any form
2. Look for `{% csrf_token %}`

**Expected Result:**
- ✓ Hidden input: `<input type="hidden" name="csrfmiddlewaretoken" value="...">`
- ✓ Present in ALL forms
- ✓ Different per session

**Pass/Fail:** _______

---

### TC-06-11: CSRF Token Validation
**Purpose:** Verify form submission requires valid token

**Steps:**
1. Remove CSRF token from form
2. Try to submit

**Expected Result:**
- ✓ Error: "CSRF verification failed"
- ✓ Form not processed
- ✓ Request rejected

**Pass/Fail:** _______

---

## Test Suite: File Upload Security

### TC-06-12: Invalid File Type Rejected
**Purpose:** Verify only images allowed

**Steps:**
1. Try to upload .exe file as product image
2. Submit form

**Expected Result:**
- ✓ Error: "Invalid file type"
- ✓ Upload rejected
- ✓ Only JPG, PNG, GIF allowed

**Pass/Fail:** _______

---

### TC-06-13: Oversized File Rejected
**Purpose:** Verify file size limit

**Steps:**
1. Try to upload 10MB image
2. Submit

**Expected Result:**
- ✓ Error: "File too large (max 5MB)"
- ✓ Upload blocked

**Pass/Fail:** _______

---

### TC-06-14: File Stored in Media Folder
**Purpose:** Verify uploads isolated from code

**Steps:**
1. Upload valid product image
2. Check filesystem

**Expected Result:**
- ✓ Image saved in `media/` folder
- ✓ NOT in code directories
- ✓ Separate from templates/static

**Pass/Fail:** _______

---

## Test Suite: XSS Protection

### TC-06-15: HTML Escaped in Output
**Purpose:** Verify user input sanitized

**Steps:**
1. Create product with name: `<script>alert('XSS')</script>`
2. View product list

**Expected Result:**
- ✓ Script NOT executed
- ✓ Displayed as text: `&lt;script&gt;...`
- ✓ Django auto-escapes HTML

**Pass/Fail:** _______

---

### TC-06-16: Safe String Handling
**Purpose:** Verify comments don't execute code

**Steps:**
1. Leave review with comment: `<img src=x onerror=alert('XSS')>`
2. View review

**Expected Result:**
- ✓ Tag displayed as text
- ✓ NOT rendered as HTML
- ✓ No script execution

**Pass/Fail:** _______

---

## Test Suite: Token Expiration

### TC-06-17: Password Reset Token Expires
**Purpose:** Verify 5-minute expiration

**Steps:**
1. Request reset link
2. Wait 6 minutes
3. Try to use link

**Expected Result:**
- ✓ Error: "This reset link has expired"
- ✓ Token not accepted
- ✓ Must request new one

**Pass/Fail:** _______

---

### TC-06-18: Token Single Use
**Purpose:** Verify token deleted after use

**Steps:**
1. Use reset link (succeeds)
2. Try to use same link again

**Expected Result:**
- ✓ Error: "Invalid or expired token"
- ✓ Token deleted from database
- ✓ Cannot reuse

**Pass/Fail:** _______

---

### TC-06-19: Token Generation Secure
**Purpose:** Verify unpredictable tokens

**Steps:**
1. Request 3 reset links
2. Compare tokens

**Expected Result:**
- ✓ All tokens different
- ✓ SHA-1 hash (64 chars)
- ✓ Not predictable

**Pass/Fail:** _______

---

## Test Suite: Transaction Integrity

### TC-06-20: Checkout Uses Transaction
**Purpose:** Verify atomic operation

**Steps:**
1. Add product to cart
2. Modify code to fail after order creation (test env)
3. Try to checkout

**Expected Result:**
- ✓ Order NOT created
- ✓ Stock NOT reduced
- ✓ Cart NOT cleared
- ✓ All-or-nothing (rollback)

**Pass/Fail:** _______ (Requires code modification)

---

### TC-06-21: Foreign Key Constraints
**Purpose:** Verify referential integrity

**Steps:**
1. Try to delete product that's in an order
2. Via admin or database

**Expected Result:**
- ✓ Error: "Cannot delete - referenced by orders"
- ✓ PROTECT constraint enforced
- ✓ Data integrity maintained

**Pass/Fail:** _______

---

## Test Suite: Admin Panel Security

### TC-06-22: Admin Requires Staff Status
**Purpose:** Verify regular users blocked

**Steps:**
1. Create user (not staff)
2. Try to access `/admin/`

**Expected Result:**
- ✓ Login page shown OR
- ✓ Error: "You don't have permission"
- ✓ Cannot access admin

**Pass/Fail:** _______

---

### TC-06-23: Admin Panel Accessible
**Purpose:** Verify superuser can access

**Steps:**
1. Login as superuser
2. Navigate to `/admin/`

**Expected Result:**
- ✓ Admin dashboard loads
- ✓ All models visible
- ✓ Can manage data

**Pass/Fail:** _______

---

### TC-06-24: Admin Can View Orders
**Purpose:** Verify order management in admin

**Steps:**
1. Login to admin
2. Go to Orders section

**Expected Result:**
- ✓ All orders listed
- ✓ Order items shown inline
- ✓ Can change order status
- ✓ Cannot delete orders

**Pass/Fail:** _______

---

## Test Suite: Error Handling

### TC-06-25: 404 Page Not Found
**Purpose:** Verify invalid URLs handled

**Steps:**
1. Navigate to `/nonexistent-page/`

**Expected Result:**
- ✓ 404 error page shown
- ✓ User-friendly message
- ✓ Link back to homepage

**Pass/Fail:** _______

---

### TC-06-26: 403 Forbidden
**Purpose:** Verify unauthorized access blocked

**Steps:**
1. As buyer, try to access `/stores/` directly

**Expected Result:**
- ✓ 403 or redirect
- ✓ Error message shown
- ✓ Access denied

**Pass/Fail:** _______

---

### TC-06-27: Form Validation Errors
**Purpose:** Verify errors display properly

**Steps:**
1. Submit incomplete form
2. Check error messages

**Expected Result:**
- ✓ Errors shown per field
- ✓ Red text
- ✓ Clear instructions
- ✓ Form not submitted

**Pass/Fail:** _______

---

## Test Suite: Data Validation

### TC-06-28: Stock Cannot Be Negative
**Purpose:** Verify stock validation

**Steps:**
1. Try to create product with stock = -5
2. OR try to edit to negative

**Expected Result:**
- ✓ Error or HTML validation blocks it
- ✓ Stock must be >= 0

**Pass/Fail:** _______

---

### TC-06-29: Price Must Be Positive
**Purpose:** Verify price validation

**Steps:**
1. Try to set price to 0 or negative

**Expected Result:**
- ✓ Error: "Price must be greater than 0"
- ✓ Form not submitted

**Pass/Fail:** _______

---

### TC-06-30: Email Format Validation
**Purpose:** Verify email validated

**Steps:**
1. Try to register with email: "notanemail"
2. Submit

**Expected Result:**
- ✓ Error: "Enter a valid email address"
- ✓ Form not submitted

**Pass/Fail:** _______

---

## Test Summary

**Total Tests:** 30
**Category:** Security & Permissions
**Priority:** CRITICAL (Security essential)
**Dependencies:** All other tests

**Results:**
- Passed: ___ / 30
- Failed: ___ / 30
- Blocked: ___ / 30

---

## Security Checklist

**Authentication:**
- ✓ Password hashing (PBKDF2)
- ✓ Session management
- ✓ Login required decorators
- ✓ Token expiration

**Authorization:**
- ✓ Group-based permissions
- ✓ Ownership validation
- ✓ Admin panel restricted

**Data Security:**
- ✓ SQL injection prevention
- ✓ XSS protection
- ✓ CSRF protection
- ✓ File upload validation

**Session Security:**
- ✓ HTTP-only cookies
- ✓ Session timeout
- ✓ Server-side storage

**Database:**
- ✓ Foreign key constraints
- ✓ Transaction management
- ✓ MariaDB backend
