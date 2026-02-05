# ECOMMERCE TEST SUITE - INDEX

## Overview
This test suite covers all features of the eCommerce web application. Tests are organized by functional area for easier execution and tracking.

---

## Test Files

### authentication.md
**Tests:** 16
**Focus:** User registration, login, logout, password reset
**Priority:** HIGH

**Key Areas:**
- Vendor registration
- Buyer registration
- Login/logout
- Password reset flow
- Token expiration
- Session management

---

### store_management.md
**Tests:** 17
**Focus:** Store CRUD operations, ownership validation
**Priority:** HIGH

**Key Areas:**
- Create store
- View stores
- Edit store
- Delete store
- Store permissions
- Store-product relationship

---

### product_management.md
**Tests:** 25
**Focus:** Product CRUD, stock management, image upload
**Priority:** HIGH

**Key Areas:**
- Add products
- Stock status (3-tier system)
- Edit products
- Delete products
- Image upload
- Product permissions
- Category assignment

---

### cart_checkout.md
**Tests:** 28
**Focus:** Cart operations, checkout process, order creation
**Priority:** CRITICAL

**Key Areas:**
- Add to cart
- View cart
- Update quantities
- Remove items
- Cart persistence
- Checkout flow
- Stock validation
- Order confirmation
- Order history

---

### review_system.md
**Tests:** 23
**Focus:** Product reviews, verified vs unverified
**Priority:** HIGH

**Key Areas:**
- Submit reviews
- Verified reviews (purchased)
- Unverified reviews
- Edit reviews
- Delete reviews
- Review display
- Duplicate prevention
- Verification logic

---

### security_permissions.md
**Tests:** 30
**Focus:** Security measures, permissions, data validation
**Priority:** CRITICAL

**Key Areas:**
- Email system
- Database security
- Session security
- CSRF protection
- XSS protection
- File upload security
- Token expiration
- Transaction integrity
- Admin panel
- Error handling

---

## Total Test Summary

| Test File | Test Count | Priority | Dependencies |
|-----------|------------|----------|--------------|
| authentication.md | 16 | HIGH | None |
| store_management.md | 17 | HIGH | authentication |
| product_management.md | 25 | HIGH | authentication, store_management |
| cart_checkout.md | 28 | CRITICAL | authentication, product_management |
| review_system.md | 23 | HIGH | authentication, product_management, cart_checkout |
| security_permissions.md | 30 | CRITICAL | All above |
| **TOTAL** | **139** | | |

---

## Test Execution Order

**Recommended Sequence:**
1. **authentication.md** - Must pass first (enables all features)
2. **store_management.md** - Vendors need stores
3. **product_management.md** - Products need stores
4. **cart_checkout.md** - Shopping requires products
5. **review_system.md** - Reviews require purchases
6. **security_permissions.md** - Tests all features

---

## Quick Start: Running Tests

### Setup Test Environment
```bash
# Navigate to project
cd eCommerce

# Ensure MariaDB is running
# Ensure server is running
python manage.py runserver
```

### Create Test Data
**Create these test accounts:**
```
Vendor 1:
- Username: testvendor1
- Email: vendor1@test.com
- Password: vendor123
- Type: Vendor

Buyer 1:
- Username: testbuyer1
- Email: buyer1@test.com
- Password: buyer123
- Type: Buyer
```

**As Vendor1, create:**
- 1 store (active)
- 3 products (varying stock: 0, 5, 50)

---

## Test Execution Guide

### Step-by-Step Process:

1. **Open test file** (start with `authentication.md`)
2. **Read each test case** carefully
3. **Execute the steps** in your browser
4. **Check expected results**
5. **Mark Pass/Fail** on each test
6. **Note any bugs** found
7. **Move to next test file**

### Example Test Execution:

**From authentication.md - TC-01-01:**
```
1. Navigate to /accounts/register/
2. Enter: testvendor1, vendor1@test.com, vendor123
3. Select: Vendor
4. Click "Register"
5. Check: Redirected to welcome, "Vendors" group assigned
6. Mark: PASS ✓ or FAIL ✗
```

---

## Test Results Tracking

### Results Template:
```
ECOMMERCE TEST RESULTS
Date: January 23, 2026
Tester: [Your Name]

authentication.md:           ___ / 16  passed
store_management.md:         ___ / 17  passed
product_management.md:       ___ / 25  passed
cart_checkout.md:            ___ / 28  passed
review_system.md:            ___ / 23  passed
security_permissions.md:     ___ / 30  passed

TOTAL:                       ___ / 139 passed

Critical Issues: ___
High Priority Issues: ___
Notes: _______________
```

---

## Test Completion Criteria

**Ready for submission when:**
- ✓ All 139 test cases executed
- ✓ Critical tests: 100% pass
- ✓ High priority tests: 100% pass
- ✓ All bugs documented
- ✓ Planning documents complete

---

## Quick Reference

**Test Data Needed:**
- 2 vendors
- 2 buyers  
- 3 stores
- 4 products (varying stock)

**Tools Needed:**
- Web browser (Chrome recommended)
- Django server running
- MariaDB running
- Text editor (for tracking results)

---

## Files to Monitor During Testing

**Directories:**
- `eCommerce/emails/` - Check invoice emails
- Django admin panel - Verify data
- Browser console - Check for errors

**Database:**
- Use admin panel to verify data
- Check user groups
- Verify orders created

---

## Next Steps

1. **Close VS Code files** (old TEST_XX files don't exist anymore)
2. **Start server:** `python manage.py runserver`
3. **Open:** `authentication.md` 
4. **Begin testing** from TC-01-01
5. **Track results** as you go

**Ready to start testing!** 🚀

## Overview
This test suite covers all features of the eCommerce web application. Tests are organized by functional area for easier execution and tracking.

---

## Test Files

### TEST_01: Authentication System
**File:** `TEST_01_authentication.md`
**Tests:** 16
**Focus:** User registration, login, logout, password reset
**Priority:** HIGH

**Key Areas:**
- Vendor registration
- Buyer registration
- Login/logout
- Password reset flow
- Token expiration
- Session management

---

### TEST_02: Store Management (Vendors)
**File:** `TEST_02_store_management.md`
**Tests:** 17
**Focus:** Store CRUD operations, ownership validation
**Priority:** HIGH

**Key Areas:**
- Create store
- View stores
- Edit store
- Delete store
- Store permissions
- Store-product relationship

---

### TEST_03: Product Management (Vendors)
**File:** `TEST_03_product_management.md`
**Tests:** 25
**Focus:** Product CRUD, stock management, image upload
**Priority:** HIGH

**Key Areas:**
- Add products
- Stock status (3-tier system)
- Edit products
- Delete products
- Image upload
- Product permissions
- Category assignment

---

### TEST_04: Shopping Cart & Checkout (Buyers)
**File:** `TEST_04_cart_checkout.md`
**Tests:** 28
**Focus:** Cart operations, checkout process, order creation
**Priority:** CRITICAL

**Key Areas:**
- Add to cart
- View cart
- Update quantities
- Remove items
- Cart persistence
- Checkout flow
- Stock validation
- Order confirmation
- Order history

---

### TEST_05: Review System (Buyers)
**File:** `TEST_05_review_system.md`
**Tests:** 23
**Focus:** Product reviews, verified vs unverified
**Priority:** HIGH

**Key Areas:**
- Submit reviews
- Verified reviews (purchased)
- Unverified reviews
- Edit reviews
- Delete reviews
- Review display
- Duplicate prevention
- Verification logic

---

### TEST_06: Security & Permissions
**File:** `TEST_06_security_permissions.md`
**Tests:** 30
**Focus:** Security measures, permissions, data validation
**Priority:** CRITICAL

**Key Areas:**
- Email system
- Database security
- Session security
- CSRF protection
- XSS protection
- File upload security
- Token expiration
- Transaction integrity
- Admin panel
- Error handling

---

## Total Test Summary

| Test File | Test Count | Priority | Dependencies |
|-----------|------------|----------|--------------|
| TEST_01 | 16 | HIGH | None |
| TEST_02 | 17 | HIGH | TEST_01 |
| TEST_03 | 25 | HIGH | TEST_01, TEST_02 |
| TEST_04 | 28 | CRITICAL | TEST_01, TEST_03 |
| TEST_05 | 23 | HIGH | TEST_01, TEST_03, TEST_04 |
| TEST_06 | 30 | CRITICAL | All above |
| **TOTAL** | **139** | | |

---

## Test Execution Order

**Recommended Sequence:**
1. TEST_01 - Authentication (must pass first)
2. TEST_02 - Store Management
3. TEST_03 - Product Management
4. TEST_04 - Cart & Checkout
5. TEST_05 - Review System
6. TEST_06 - Security & Permissions

**Rationale:**
- Authentication enables all other features
- Store required before products
- Products required before cart
- Cart required before reviews (for verified)
- Security tests all features

---

## Test Data Requirements

### Users Needed
```
Vendor1:
- Username: testvendor1
- Email: vendor1@test.com
- Password: vendor123
- Group: Vendors

Vendor2:
- Username: testvendor2
- Email: vendor2@test.com
- Password: vendor123
- Group: Vendors

Buyer1:
- Username: testbuyer1
- Email: buyer1@test.com
- Password: buyer123
- Group: Buyers

Buyer2:
- Username: testbuyer2
- Email: buyer2@test.com
- Password: buyer123
- Group: Buyers
```

### Stores Needed
```
Store1 (Vendor1):
- Name: Electronics Hub
- Active: True

Store2 (Vendor1):
- Name: Fashion Corner
- Active: False

Store3 (Vendor2):
- Name: Book World
- Active: True
```

### Products Needed
```
Product A (Store1):
- Name: Laptop
- Price: R 2500
- Stock: 10
- Category: Electronics

Product B (Store1):
- Name: Mouse
- Price: R 150
- Stock: 5
- Category: Electronics

Product C (Store2):
- Name: T-Shirt
- Price: R 250
- Stock: 0
- Category: Clothing

Product D (Store3):
- Name: Novel
- Price: R 180
- Stock: 15
- Category: Books
```

---

## Test Tracking

### Status Codes
- **PASS** - Test passed successfully
- **FAIL** - Test failed (bug found)
- **BLOCKED** - Cannot test (dependency failed)
- **SKIP** - Not applicable/implemented

### Results Template
```
Test File: TEST_XX
Date Tested: ___________
Tester: ___________

Results:
- Passed: ___ / ___
- Failed: ___ / ___
- Blocked: ___ / ___
- Skipped: ___ / ___

Notes:
_______________________
_______________________
```

---

## Quick Start Guide

### 1. Setup Test Environment
```bash
cd eCommerce
python manage.py migrate
python manage.py createsuperuser
```

### 2. Create Test Users
- Register vendor1, vendor2 (via /accounts/register/)
- Register buyer1, buyer2 (via /accounts/register/)

### 3. Create Test Data
- Login as vendor1 → create 2 stores
- Add products to stores
- Vary stock levels (0, 5, 10+)

### 4. Execute Tests
- Follow each test file sequentially
- Mark PASS/FAIL on each test case
- Note any bugs found

### 5. Report Results
- Count passed vs failed
- List critical failures
- Document bugs for fixing

---

## Known Limitations

**Not Tested (Future):**
- Payment processing (not implemented)
- Shipping calculator (not implemented)
- Product search (not implemented)
- Automated tests (manual only)
- Performance/load testing
- Browser compatibility (manual check only)

---

## Testing Tools

**Manual Testing:**
- Web browser (Chrome recommended)
- Django admin panel
- MariaDB command line (optional)
- Text editor (for tracking results)

**Files to Monitor:**
- `eCommerce/emails/` - Invoice and reset emails
- Database (via admin or dbshell)
- Browser console (for JavaScript errors)

---

## Bug Reporting Template

```
Bug ID: #___
Test Case: TC-XX-XX
Date Found: ___________
Severity: Critical / High / Medium / Low

Description:
_______________________

Steps to Reproduce:
1. _______________________
2. _______________________
3. _______________________

Expected Result:
_______________________

Actual Result:
_______________________

Screenshots/Logs:
_______________________
```

---

## Test Completion Criteria

**All tests pass when:**
- ✓ All 139 test cases executed
- ✓ Critical failures: 0
- ✓ High priority failures: 0
- ✓ Medium/Low failures: Documented and acceptable
- ✓ All core features functional
- ✓ Security tests pass

**Ready for submission when:**
- ✓ Test completion criteria met
- ✓ Bug fixes implemented (if needed)
- ✓ Re-tested after fixes
- ✓ Test results documented
- ✓ Planning documents complete

---

## Contact

**For questions about tests:**
- Refer to individual test files for details
- Check Planning documents for requirements
- Review code for implementation details
