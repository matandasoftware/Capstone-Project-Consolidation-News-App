# TEST 03: PRODUCT MANAGEMENT (VENDORS)

## Test Suite: Add Products

### TC-03-01: Add Product - Complete Data
**Purpose:** Verify vendor can add product with all fields

**Precondition:** Logged in as vendor with at least one store

**Steps:**
1. Go to "My Products"
2. Click "Add New Product"
3. Fill all fields:
   - Name: Laptop
   - Store: Select owned store
   - Category: Electronics
   - Description: High-performance laptop
   - Price: 2500.00
   - Stock: 25
   - Image: Upload laptop.jpg
   - Active: ✓ Checked
4. Click "Create Product"

**Expected Result:**
- ✓ Product created in database
- ✓ Image uploaded to media folder
- ✓ Appears in store detail page
- ✓ Success message shown
- ✓ Redirected to store detail or product list

**Pass/Fail:** _______

---

### TC-03-02: Add Product - Minimum Required Fields
**Purpose:** Verify only required fields needed

**Steps:**
1. Create product with:
   - Name: Mouse
   - Store: Select store
   - Description: Wireless mouse
   - Price: 150.00
   - Stock: 10
   - (No category, no image)
2. Submit

**Expected Result:**
- ✓ Product created
- ✓ Shows placeholder image
- ✓ Category shown as "Uncategorized" or blank

**Pass/Fail:** _______

---

### TC-03-03: Add Product - Missing Required Field
**Purpose:** Verify validation on required fields

**Steps:**
1. Try to create product without name
2. Submit

**Expected Result:**
- ✓ Error: "This field is required" on name
- ✓ Form not submitted
- ✓ Product not created

**Pass/Fail:** _______

---

### TC-03-04: Add Product - Invalid Price
**Purpose:** Verify price validation

**Steps:**
1. Enter price: -50 (negative)
2. Submit

**Expected Result:**
- ✓ Error: "Price must be positive"
- ✓ Form not submitted

**Alternative:**
1. Enter price: "abc" (text)
2. **Expected:** Browser validation or error message

**Pass/Fail:** _______

---

### TC-03-05: Add Product - Invalid Stock
**Purpose:** Verify stock validation

**Steps:**
1. Enter stock: -5 (negative)
2. Submit

**Expected Result:**
- ✓ Error or prevented by HTML validation
- ✓ Stock must be >= 0

**Pass/Fail:** _______

---

### TC-03-06: Add Product - Store Dropdown
**Purpose:** Verify only owned stores appear

**Precondition:**
- Vendor1 has Store A and Store B
- Vendor2 has Store C

**Steps:**
1. Login as Vendor1
2. View add product form
3. Check store dropdown

**Expected Result:**
- ✓ Shows Store A
- ✓ Shows Store B
- ✓ Does NOT show Store C

**Pass/Fail:** _______

---

## Test Suite: Stock Status Display

### TC-03-07: Stock Status - Out of Stock (0)
**Purpose:** Verify 0 stock shows red badge

**Steps:**
1. Create product with stock = 0
2. View product list

**Expected Result:**
- ✓ Red badge: "Out of Stock"
- ✓ No quantity shown
- ✓ No "Add to Cart" button for buyers

**Pass/Fail:** _______

---

### TC-03-08: Stock Status - In Store Only (1-10)
**Purpose:** Verify low stock shows orange badge

**Steps:**
1. Create product with stock = 5
2. View product list

**Expected Result:**
- ✓ Orange badge: "In Store Only (5 left)"
- ✓ Quantity shown
- ✓ "Add to Cart" available

**Pass/Fail:** _______

---

### TC-03-09: Stock Status - In Stock (11+)
**Purpose:** Verify high stock shows green badge

**Steps:**
1. Create product with stock = 50
2. View product list

**Expected Result:**
- ✓ Green badge: "In Stock (50)"
- ✓ Quantity shown
- ✓ "Add to Cart" available

**Pass/Fail:** _______

---

### TC-03-10: Stock Status - Update After Sale
**Purpose:** Verify stock reduces after purchase

**Precondition:** Product has stock = 10

**Steps:**
1. Buyer purchases 3 units (checkout)
2. View product again

**Expected Result:**
- ✓ Stock now = 7
- ✓ Badge updates: "In Store Only (7 left)"

**Pass/Fail:** _______

---

## Test Suite: Edit Products

### TC-03-11: Edit Product - Update Price
**Purpose:** Verify product can be edited

**Steps:**
1. Click "Edit" on product
2. Change price from 2500 to 2000
3. Save

**Expected Result:**
- ✓ Price updated
- ✓ Success message
- ✓ New price shown everywhere
- ✓ Past orders still show old price

**Pass/Fail:** _______

---

### TC-03-12: Edit Product - Change Stock
**Purpose:** Verify stock can be adjusted

**Steps:**
1. Edit product
2. Change stock from 25 to 0
3. Save

**Expected Result:**
- ✓ Stock updated to 0
- ✓ Badge changes to "Out of Stock"
- ✓ "Add to Cart" disabled

**Pass/Fail:** _______

---

### TC-03-13: Edit Product - Replace Image
**Purpose:** Verify image can be changed

**Steps:**
1. Edit product
2. Upload new image
3. Save

**Expected Result:**
- ✓ Old image replaced
- ✓ New image displayed
- ✓ Old image file removed (optional)

**Pass/Fail:** _______

---

### TC-03-14: Edit Product - Toggle Active Status
**Purpose:** Verify product can be deactivated

**Steps:**
1. Edit product
2. Uncheck "Active"
3. Save

**Expected Result:**
- ✓ Product marked inactive
- ✓ Not visible in public product list
- ✓ Still visible in vendor's "My Products"
- ✓ Can be reactivated later

**Pass/Fail:** _______

---

## Test Suite: Delete Products

### TC-03-15: Delete Product - Confirmation
**Purpose:** Verify delete shows confirmation

**Steps:**
1. Click "Delete" on product
2. View confirmation page

**Expected Result:**
- ✓ Warning message shown
- ✓ Product name displayed
- ✓ "Confirm Delete" button
- ✓ "Cancel" button

**Pass/Fail:** _______

---

### TC-03-16: Delete Product - Not in Orders
**Purpose:** Verify product without orders can be deleted

**Precondition:** Product has no order history

**Steps:**
1. Delete product (confirm)

**Expected Result:**
- ✓ Product deleted from database
- ✓ Image file deleted (optional)
- ✓ Success message
- ✓ Product no longer appears

**Pass/Fail:** _______

---

### TC-03-17: Delete Product - In Past Orders
**Purpose:** Verify product in orders cannot be deleted

**Precondition:** Product is in completed order

**Steps:**
1. Try to delete product

**Expected Result:**
- ✓ Error: "Cannot delete product in orders"
- ✓ OR success with product marked inactive
- ✓ Order history preserved

**Note:** Current implementation uses PROTECT constraint

**Pass/Fail:** _______

---

## Test Suite: Image Upload

### TC-03-18: Upload Valid Image
**Purpose:** Verify image upload works

**Steps:**
1. Upload JPG image (2MB)
2. Save product

**Expected Result:**
- ✓ Image uploaded to media folder
- ✓ Image displayed in product card
- ✓ Image path stored in database

**Pass/Fail:** _______

---

### TC-03-19: Upload Invalid Format
**Purpose:** Verify only allowed formats accepted

**Steps:**
1. Try to upload .exe file
2. Submit

**Expected Result:**
- ✓ Error: "Invalid file format"
- ✓ Only JPG, PNG, GIF allowed
- ✓ Product not created

**Pass/Fail:** _______

---

### TC-03-20: Upload Oversized Image
**Purpose:** Verify file size limit

**Steps:**
1. Try to upload 10MB image
2. Submit

**Expected Result:**
- ✓ Error: "File too large (max 5MB)"
- ✓ Upload rejected

**Pass/Fail:** _______

---

## Test Suite: Permissions

### TC-03-21: Buyer Cannot Add Product
**Purpose:** Verify buyers blocked

**Precondition:** Logged in as buyer

**Steps:**
1. Try to access `/vendor/product/new/`

**Expected Result:**
- ✓ Error: "Access denied"
- ✓ "My Products" not in navigation

**Pass/Fail:** _______

---

### TC-03-22: Cannot Edit Other Vendor's Product
**Purpose:** Verify product ownership enforced

**Precondition:**
- Vendor1 has product ID=5
- Logged in as Vendor2

**Steps:**
1. Try to access `/vendor/product/5/edit/`

**Expected Result:**
- ✓ Error: "Access denied"
- ✓ Product not editable

**Pass/Fail:** _______

---

### TC-03-23: Vendor Product List - Own Products Only
**Purpose:** Verify vendor sees only their products

**Precondition:**
- Vendor1 has 5 products
- Vendor2 has 3 products

**Steps:**
1. Login as Vendor1
2. Go to "My Products"

**Expected Result:**
- ✓ Shows 5 products (Vendor1's only)
- ✓ Does NOT show Vendor2's products

**Pass/Fail:** _______

---

## Test Suite: Category Assignment

### TC-03-24: Product with Category
**Purpose:** Verify category assignment works

**Steps:**
1. Create product
2. Select category: Electronics
3. Save

**Expected Result:**
- ✓ Product associated with category
- ✓ Category shown on product detail
- ✓ Product appears in category filter

**Pass/Fail:** _______

---

### TC-03-25: Product Without Category
**Purpose:** Verify category is optional

**Steps:**
1. Create product
2. Leave category empty
3. Save

**Expected Result:**
- ✓ Product created successfully
- ✓ Category shown as blank or "Uncategorized"

**Pass/Fail:** _______

---

## Test Data Setup

**Test Products:**
```
Product 1 (Vendor1, Store1):
- Name: Laptop
- Price: R 2500.00
- Stock: 25
- Category: Electronics
- Active: True

Product 2 (Vendor1, Store1):
- Name: Mouse
- Price: R 150.00
- Stock: 5
- Category: Electronics
- Active: True

Product 3 (Vendor1, Store2):
- Name: T-Shirt
- Price: R 250.00
- Stock: 0
- Category: Clothing
- Active: True

Product 4 (Vendor2, Store3):
- Name: Novel
- Price: R 180.00
- Stock: 15
- Category: Books
- Active: True
```

---

## Test Summary

**Total Tests:** 25
**Category:** Product Management (Vendor Feature)
**Priority:** HIGH
**Dependencies:**
- Authentication tests
- Store management tests

**Results:**
- Passed: ___ / 25
- Failed: ___ / 25
- Blocked: ___ / 25

---

## Notes

**Stock Validation:**
- Must be integer >= 0
- Updates automatically after purchase
- Three-tier display system

**Ownership:**
- Vendor can only manage products in own stores
- PROTECT constraint prevents deletion if in orders

**Image Upload:**
- Allowed: JPG, PNG, GIF
- Max size: 5MB
- Stored in media folder
