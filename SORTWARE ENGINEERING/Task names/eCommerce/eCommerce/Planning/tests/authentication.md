# TEST 01: AUTHENTICATION SYSTEM

## Test Suite: User Registration & Login

### TC-01-01: Vendor Registration - Valid Data
**Purpose:** Verify vendor can register successfully

**Steps:**
1. Navigate to `/accounts/register/`
2. Enter:
   - Username: testvendor1
   - Email: vendor@test.com
   - Password: test1234
   - Confirm: test1234
   - Type: Vendor
3. Click "Register"

**Expected Result:**
- ✓ User created in database
- ✓ Assigned to "Vendors" group
- ✓ Redirected to welcome page
- ✓ Success message shown

**Pass/Fail:** _______

---

### TC-01-02: Buyer Registration - Valid Data
**Purpose:** Verify buyer can register successfully

**Steps:**
1. Navigate to `/accounts/register/`
2. Enter valid data with Type: Buyer
3. Submit form

**Expected Result:**
- ✓ User created
- ✓ Assigned to "Buyers" group
- ✓ Redirected to welcome

**Pass/Fail:** _______

---

### TC-01-03: Registration - Duplicate Username
**Purpose:** Verify duplicate username rejected

**Steps:**
1. Register user "testuser1"
2. Try to register another user "testuser1"

**Expected Result:**
- ✓ Error: "This username is already taken"
- ✓ Form not submitted
- ✓ User can choose different username

**Pass/Fail:** _______

---

### TC-01-04: Registration - Duplicate Email
**Purpose:** Verify duplicate email rejected

**Steps:**
1. Register with test@example.com
2. Try to register another user with same email

**Expected Result:**
- ✓ Error shown
- ✓ Registration blocked

**Pass/Fail:** _______

---

### TC-01-05: Registration - Password Mismatch
**Purpose:** Verify password confirmation works

**Steps:**
1. Enter Password: "test1234"
2. Enter Confirm: "different123"
3. Submit

**Expected Result:**
- ✓ Error: "Passwords don't match"
- ✓ Form not submitted

**Pass/Fail:** _______

---

### TC-01-06: Registration - Missing Required Fields
**Purpose:** Verify all required fields validated

**Steps:**
1. Submit empty registration form

**Expected Result:**
- ✓ Error on username: "This field is required"
- ✓ Error on email: "This field is required"
- ✓ Error on password: "This field is required"
- ✓ Form not submitted

**Pass/Fail:** _______

---

### TC-01-07: Login - Valid Credentials
**Purpose:** Verify login works with correct credentials

**Precondition:** User "testuser" exists with password "test1234"

**Steps:**
1. Navigate to `/accounts/login/`
2. Enter username: testuser
3. Enter password: test1234
4. Click "Login"

**Expected Result:**
- ✓ Session created
- ✓ User redirected to dashboard
- ✓ Navigation shows "Welcome, testuser"
- ✓ Logout button visible

**Pass/Fail:** _______

---

### TC-01-08: Login - Invalid Password
**Purpose:** Verify wrong password rejected

**Steps:**
1. Enter username: testuser
2. Enter password: wrongpassword
3. Click "Login"

**Expected Result:**
- ✓ Error: "Invalid username or password"
- ✓ Remain on login page
- ✓ No session created

**Pass/Fail:** _______

---

### TC-01-09: Login - Invalid Username
**Purpose:** Verify non-existent user rejected

**Steps:**
1. Enter username: nonexistentuser
2. Enter any password
3. Submit

**Expected Result:**
- ✓ Error: "Invalid username or password"
- ✓ No session created

**Pass/Fail:** _______

---

### TC-01-10: Logout
**Purpose:** Verify logout clears session

**Precondition:** User logged in

**Steps:**
1. Click "Logout" in navigation
2. Confirm logout

**Expected Result:**
- ✓ Redirected to login page
- ✓ Success message: "You have been logged out"
- ✓ Cart preserved (optional feature)
- ✓ Navigation shows Login/Register

**Pass/Fail:** _______

---

### TC-01-11: Session Timeout
**Purpose:** Verify session expires after 10 minutes

**Steps:**
1. Login successfully
2. Wait 11 minutes (no activity)
3. Try to access protected page

**Expected Result:**
- ✓ Error: "Your session has expired"
- ✓ Redirected to login
- ✓ Must login again

**Pass/Fail:** _______

---

## Test Suite: Password Reset

### TC-01-12: Password Reset - Valid Email
**Purpose:** Verify password reset email sent

**Precondition:** User with email test@example.com exists

**Steps:**
1. Go to login page
2. Click "Forgot Password?"
3. Enter: test@example.com
4. Click "Send Reset Link"

**Expected Result:**
- ✓ Success message shown
- ✓ Email file created in `emails/` folder
- ✓ Email contains reset link
- ✓ Token valid for 5 minutes

**Pass/Fail:** _______

---

### TC-01-13: Password Reset - Complete Flow
**Purpose:** Verify full password reset works

**Steps:**
1. Request reset link
2. Open email file in `emails/`
3. Copy reset URL
4. Navigate to reset URL
5. Enter new password: newpass123
6. Confirm new password: newpass123
7. Submit

**Expected Result:**
- ✓ Success message: "Password changed"
- ✓ Redirected to login
- ✓ Can login with new password
- ✓ Old password no longer works

**Pass/Fail:** _______

---

### TC-01-14: Password Reset - Token Expiration
**Purpose:** Verify token expires after 5 minutes

**Steps:**
1. Request reset link
2. Copy URL from email
3. Wait 6 minutes
4. Try to use reset URL

**Expected Result:**
- ✓ Error: "This reset link has expired"
- ✓ Link to request new token
- ✓ Password not changed

**Pass/Fail:** _______

---

### TC-01-15: Password Reset - Token Reuse
**Purpose:** Verify token only works once

**Steps:**
1. Request reset link
2. Use link to reset password (succeeds)
3. Try to use same link again

**Expected Result:**
- ✓ Error: "Invalid or expired token"
- ✓ Token deleted from database
- ✓ Must request new token

**Pass/Fail:** _______

---

### TC-01-16: Password Reset - Non-Existent Email
**Purpose:** Verify security (no email enumeration)

**Steps:**
1. Request reset for nonexistent@test.com
2. Submit

**Expected Result:**
- ✓ Generic success message (for security)
- ✓ No email sent
- ✓ No error revealing email doesn't exist

**Pass/Fail:** _______

---

## Test Data Setup

**Test Users:**
```
Vendor:
- Username: testvendor
- Email: vendor@test.com
- Password: vendor123
- Group: Vendors

Buyer:
- Username: testbuyer
- Email: buyer@test.com
- Password: buyer123
- Group: Buyers
```

---

## Test Summary

**Total Tests:** 16
**Category:** Authentication & Security
**Priority:** HIGH (Core functionality)
**Dependencies:** None (can run first)

**Results:**
- Passed: ___ / 16
- Failed: ___ / 16
- Blocked: ___ / 16
