# TEST 02: STORE MANAGEMENT (VENDORS)

## Test Suite: Store CRUD Operations

### TC-02-01: Create Store - Valid Data
**Purpose:** Verify vendor can create store

**Precondition:** Logged in as vendor

**Steps:**
1. Navigate to "My Stores"
2. Click "Create New Store"
3. Enter:
   - Name: Electronics Hub
   - Description: Quality electronics
   - Active: ✓ Checked
4. Click "Create Store"

**Expected Result:**
- ✓ Store created in database
- ✓ Associated with current vendor
- ✓ Appears in "My Stores" list
- ✓ Success message shown
- ✓ Redirected to store list

**Pass/Fail:** _______

---

### TC-02-02: Create Store - Missing Name
**Purpose:** Verify name is required

**Steps:**
1. Try to create store with empty name
2. Fill description only
3. Submit

**Expected Result:**
- ✓ Error: "This field is required" for name
- ✓ Form not submitted
- ✓ Store not created

**Pass/Fail:** _______

---

### TC-02-03: Create Store - Inactive by Default
**Purpose:** Verify store can be created inactive

**Steps:**
1. Create store with:
   - Name: Test Store
   - Active: ✗ Unchecked
2. Submit

**Expected Result:**
- ✓ Store created
- ✓ Shows "Inactive" badge
- ✓ Products in store not visible to buyers

**Pass/Fail:** _______

---

### TC-02-04: View Store List
**Purpose:** Verify vendor sees only their stores

**Precondition:** Vendor has 2 stores, another vendor has 1 store

**Steps:**
1. Login as vendor1
2. Go to "My Stores"

**Expected Result:**
- ✓ Shows vendor1's 2 stores only
- ✓ Does NOT show other vendor's stores
- ✓ Shows product count per store
- ✓ Shows active/inactive status
- ✓ Shows creation date

**Pass/Fail:** _______

---

### TC-02-05: View Store Detail
**Purpose:** Verify store detail page displays correctly

**Steps:**
1. Click "View Store" on any store

**Expected Result:**
- ✓ Store name displayed
- ✓ Store description shown
- ✓ Products in store listed
- ✓ Edit/Delete buttons visible (for owner)

**Pass/Fail:** _______

---

### TC-02-06: Edit Store - Update Name
**Purpose:** Verify store can be edited

**Precondition:** Store "Test Store" exists

**Steps:**
1. Click "Edit" on Test Store
2. Change name to "Updated Store"
3. Click "Update Store"

**Expected Result:**
- ✓ Store name updated in database
- ✓ New name shown in list
- ✓ Success message
- ✓ Other fields unchanged

**Pass/Fail:** _______

---

### TC-02-07: Edit Store - Toggle Active Status
**Purpose:** Verify active status can be changed

**Steps:**
1. Edit store
2. Uncheck "Active"
3. Save

**Expected Result:**
- ✓ Store marked inactive
- ✓ Badge changes to "Inactive"
- ✓ Products no longer visible to buyers

**Verify:**
4. Re-edit store
5. Check "Active"
6. Save
- ✓ Store marked active
- ✓ Products visible again

**Pass/Fail:** _______

---

### TC-02-08: Delete Store - Confirmation
**Purpose:** Verify delete requires confirmation

**Steps:**
1. Click "Delete" on store
2. View confirmation page

**Expected Result:**
- ✓ Shows warning message
- ✓ Shows store name
- ✓ "Confirm Delete" button
- ✓ "Cancel" button
- ✓ Warns about cascade (products deleted)

**Pass/Fail:** _______

---

### TC-02-09: Delete Store - Confirmed
**Purpose:** Verify store can be deleted

**Steps:**
1. Delete store (confirm)

**Expected Result:**
- ✓ Store deleted from database
- ✓ All products in store deleted (cascade)
- ✓ Success message
- ✓ Redirected to store list
- ✓ Store no longer appears

**Pass/Fail:** _______

---

### TC-02-10: Delete Store - Cancelled
**Purpose:** Verify cancel preserves store

**Steps:**
1. Click "Delete" on store
2. Click "Cancel"

**Expected Result:**
- ✓ Store NOT deleted
- ✓ Redirected to store list
- ✓ Store still appears

**Pass/Fail:** _______

---

## Test Suite: Store Ownership & Permissions

### TC-02-11: Buyer Cannot Create Store
**Purpose:** Verify buyers blocked from vendor features

**Precondition:** Logged in as buyer

**Steps:**
1. Try to access `/stores/` directly
2. OR try to access `/store/new/`

**Expected Result:**
- ✓ Error: "Access denied"
- ✓ Redirected to appropriate page
- ✓ "My Stores" link not visible in navigation

**Pass/Fail:** _______

---

### TC-02-12: Cannot Edit Other Vendor's Store
**Purpose:** Verify store ownership enforced

**Precondition:**
- Vendor1 has store with ID=1
- Logged in as Vendor2

**Steps:**
1. Try to access `/store/1/edit/` directly

**Expected Result:**
- ✓ Error: "Access denied"
- ✓ OR 404 Not Found
- ✓ Cannot edit store

**Pass/Fail:** _______

---

### TC-02-13: Cannot Delete Other Vendor's Store
**Purpose:** Verify delete ownership enforced

**Steps:**
1. As Vendor2, try to delete Vendor1's store

**Expected Result:**
- ✓ Error shown
- ✓ Store not deleted
- ✓ Ownership validated

**Pass/Fail:** _______

---

### TC-02-14: Anonymous User Cannot Access Stores
**Purpose:** Verify login required

**Precondition:** Not logged in

**Steps:**
1. Try to access `/stores/`

**Expected Result:**
- ✓ Redirected to login page
- ✓ `?next=/stores/` in URL (return after login)

**Pass/Fail:** _______

---

## Test Suite: Store-Product Relationship

### TC-02-15: Store Shows Product Count
**Purpose:** Verify store displays number of products

**Precondition:** Store has 3 products

**Steps:**
1. View "My Stores" list

**Expected Result:**
- ✓ Store card shows "3 products"
- ✓ Count accurate
- ✓ Updates when products added/removed

**Pass/Fail:** _______

---

### TC-02-16: Delete Store Deletes Products
**Purpose:** Verify cascade deletion

**Precondition:** Store has 2 products

**Steps:**
1. Note product IDs
2. Delete store
3. Try to access product URLs

**Expected Result:**
- ✓ Store deleted
- ✓ Products also deleted
- ✓ Product pages show 404
- ✓ Products not in database

**Pass/Fail:** _______

---

### TC-02-17: Inactive Store Hides Products
**Purpose:** Verify inactive store filters products

**Precondition:** Store with 2 active products

**Steps:**
1. Set store to inactive
2. Logout
3. View public product list

**Expected Result:**
- ✓ Products from inactive store NOT shown
- ✓ Only active store products visible

**Pass/Fail:** _______

---

## Test Data Setup

**Test Stores:**
```
Store 1 (Vendor1):
- Name: Electronics Hub
- Description: Quality electronics
- Active: True
- Products: 5

Store 2 (Vendor1):
- Name: Fashion Corner
- Description: Latest trends
- Active: False
- Products: 3

Store 3 (Vendor2):
- Name: Book World
- Description: All genres
- Active: True
- Products: 2
```

---

## Test Summary

**Total Tests:** 17
**Category:** Store Management (Vendor Feature)
**Priority:** HIGH
**Dependencies:** Authentication tests must pass

**Results:**
- Passed: ___ / 17
- Failed: ___ / 17
- Blocked: ___ / 17

---

## Notes

**Cascade Deletion:**
- When store deleted, all products deleted
- Order items reference products (PROTECT)
- Cannot delete product in past orders

**Ownership Rules:**
- Vendor can only manage own stores
- Buyer cannot access store management
- Admin can manage all stores
