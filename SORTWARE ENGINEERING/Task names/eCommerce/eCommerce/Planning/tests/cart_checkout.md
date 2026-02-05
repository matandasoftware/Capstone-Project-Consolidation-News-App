# TEST 04: SHOPPING CART & CHECKOUT (BUYERS)

## Test Suite: Add to Cart

### TC-04-01: Add Product to Cart - First Item
**Purpose:** Verify buyer can add product to cart

**Precondition:**
- Logged in as buyer
- Product has stock > 0

**Steps:**
1. Navigate to product detail page
2. Click "Add to Cart"

**Expected Result:**
- ✓ Success message: "Product added to cart!"
- ✓ Cart badge shows [1]
- ✓ Product in session cart
- ✓ Redirected back to product page

**Pass/Fail:** _______

---

### TC-04-02: Add Same Product Twice
**Purpose:** Verify quantity increments

**Steps:**
1. Add product to cart (quantity = 1)
2. Add same product again

**Expected Result:**
- ✓ Cart badge shows [2]
- ✓ Session cart: `{'product_id': 2}`
- ✓ Success message shown

**Pass/Fail:** _______

---

### TC-04-03: Add Multiple Different Products
**Purpose:** Verify cart handles multiple products

**Steps:**
1. Add Product A to cart
2. Add Product B to cart
3. Add Product C to cart

**Expected Result:**
- ✓ Cart badge shows [3]
- ✓ All three products in cart
- ✓ Each tracked separately

**Pass/Fail:** _______

---

### TC-04-04: Add Out of Stock Product
**Purpose:** Verify out of stock blocked

**Precondition:** Product has stock = 0

**Steps:**
1. View product detail
2. Attempt to add to cart

**Expected Result:**
- ✓ "Add to Cart" button NOT visible
- ✓ "Out of Stock" badge shown
- ✓ Cannot add to cart

**Pass/Fail:** _______

---

### TC-04-05: Add More Than Available Stock
**Purpose:** Verify stock validation

**Precondition:** Product has stock = 5, cart already has 5

**Steps:**
1. Try to add product again (would make 6 total)

**Expected Result:**
- ✓ Warning: "Only 5 units available"
- ✓ Quantity not increased
- ✓ Cart stays at 5

**Pass/Fail:** _______

---

### TC-04-06: Vendor Cannot Add to Cart
**Purpose:** Verify vendors blocked from buying

**Precondition:** Logged in as vendor

**Steps:**
1. View product detail page

**Expected Result:**
- ✓ "Add to Cart" button NOT visible
- ✓ Message: "Login as buyer to purchase"
- ✓ Cannot access cart

**Pass/Fail:** _______

---

### TC-04-07: Anonymous Cannot Add to Cart
**Purpose:** Verify login required

**Precondition:** Not logged in

**Steps:**
1. View product detail
2. Try to add to cart (if button visible)

**Expected Result:**
- ✓ "Add to Cart" button NOT visible
- ✓ OR redirected to login
- ✓ Must login as buyer

**Pass/Fail:** _______

---

## Test Suite: View Cart

### TC-04-08: View Empty Cart
**Purpose:** Verify empty cart message

**Precondition:** Cart is empty

**Steps:**
1. Navigate to `/cart/`

**Expected Result:**
- ✓ Message: "Your cart is empty"
- ✓ Link: "Browse Products"
- ✓ No checkout button

**Pass/Fail:** _______

---

### TC-04-09: View Cart with Items
**Purpose:** Verify cart displays correctly

**Precondition:** Cart has 2 products (3 units total)

**Steps:**
1. Go to `/cart/`

**Expected Result:**
- ✓ Shows both products
- ✓ Each with: image, name, store, price, quantity, subtotal
- ✓ Shows grand total
- ✓ Shows "Proceed to Checkout" button
- ✓ Update and Remove buttons visible

**Pass/Fail:** _______

---

### TC-04-10: Cart Calculates Total Correctly
**Purpose:** Verify math is accurate

**Precondition:**
- Product A: R 100 × 2 = R 200
- Product B: R 50 × 3 = R 150

**Steps:**
1. View cart

**Expected Result:**
- ✓ Subtotal A: R 200
- ✓ Subtotal B: R 150
- ✓ Grand Total: R 350

**Pass/Fail:** _______

---

## Test Suite: Update Cart

### TC-04-11: Increase Quantity
**Purpose:** Verify quantity can be increased

**Precondition:** Product in cart with quantity = 2

**Steps:**
1. Change quantity to 5
2. Click "Update"

**Expected Result:**
- ✓ Quantity updated to 5
- ✓ Subtotal recalculated
- ✓ Total recalculated
- ✓ Success message: "Cart updated"

**Pass/Fail:** _______

---

### TC-04-12: Decrease Quantity
**Purpose:** Verify quantity can be decreased

**Steps:**
1. Change quantity from 5 to 2
2. Update

**Expected Result:**
- ✓ Quantity = 2
- ✓ Totals recalculated
- ✓ Cart badge updates

**Pass/Fail:** _______

---

### TC-04-13: Set Quantity to Zero
**Purpose:** Verify 0 removes item

**Steps:**
1. Change quantity to 0
2. Click "Update"

**Expected Result:**
- ✓ Product removed from cart
- ✓ Total recalculated
- ✓ Message: "Item removed"

**Pass/Fail:** _______

---

### TC-04-14: Exceed Available Stock
**Purpose:** Verify cannot order more than stock

**Precondition:** Product has stock = 10

**Steps:**
1. Try to set quantity to 15
2. Update

**Expected Result:**
- ✓ Warning: "Only 10 units available"
- ✓ Quantity auto-adjusted to 10
- ✓ OR blocked by max attribute

**Pass/Fail:** _______

---

## Test Suite: Remove from Cart

### TC-04-15: Remove Single Item
**Purpose:** Verify item can be removed

**Precondition:** Cart has 2 products

**Steps:**
1. Click "Remove" on Product A

**Expected Result:**
- ✓ Product A removed
- ✓ Product B remains
- ✓ Total recalculated
- ✓ Success: "Product removed from cart"

**Pass/Fail:** _______

---

### TC-04-16: Remove Last Item
**Purpose:** Verify empty cart message after last removal

**Precondition:** Cart has 1 product

**Steps:**
1. Click "Remove"

**Expected Result:**
- ✓ Product removed
- ✓ "Your cart is empty" shown
- ✓ Checkout button hidden
- ✓ Cart badge shows [0] or hidden

**Pass/Fail:** _______

---

## Test Suite: Cart Persistence

### TC-04-17: Cart Persists After Logout
**Purpose:** Verify cart preserved (optional feature)

**Steps:**
1. Add products to cart
2. Logout
3. Cart badge still shows count (if implemented)
4. Login again

**Expected Result:**
- ✓ Cart still has items
- ✓ Products preserved
- ✓ Can continue shopping

**Pass/Fail:** _______

---

### TC-04-18: Cart Survives Page Refresh
**Purpose:** Verify session-based storage works

**Steps:**
1. Add items to cart
2. Refresh page (F5)

**Expected Result:**
- ✓ Cart items still present
- ✓ Quantities preserved
- ✓ Badge shows correct count

**Pass/Fail:** _______

---

### TC-04-19: Cart Clears After Session Timeout
**Purpose:** Verify 10-minute timeout (if implemented)

**Steps:**
1. Add items to cart
2. Wait 11 minutes (no activity)
3. Try to view cart

**Expected Result:**
- ✓ Session expired message
- ✓ Must login again
- ✓ Cart may be cleared (depending on implementation)

**Pass/Fail:** _______

---

## Test Suite: Checkout Process

### TC-04-20: Checkout - Valid Order
**Purpose:** Verify checkout works end-to-end

**Precondition:** Cart has 2 products (total R 500)

**Steps:**
1. Click "Proceed to Checkout"
2. Review checkout page
3. Verify items, total, buyer info shown
4. Click "Place Order"

**Expected Result:**
- ✓ Order created in database
- ✓ Order items created
- ✓ Stock reduced for each product
- ✓ Cart cleared
- ✓ Redirected to order confirmation
- ✓ Success message with email notification
- ✓ Invoice email file created

**Pass/Fail:** _______

---

### TC-04-21: Checkout - Empty Cart
**Purpose:** Verify empty cart blocked

**Steps:**
1. Clear cart completely
2. Try to access `/checkout/` directly

**Expected Result:**
- ✓ Warning: "Your cart is empty"
- ✓ Redirected to product list
- ✓ Cannot checkout

**Pass/Fail:** _______

---

### TC-04-22: Checkout - Insufficient Stock
**Purpose:** Verify stock revalidated at checkout

**Precondition:**
- Cart has 5 units of Product A
- Another buyer purchases, leaving stock = 2

**Steps:**
1. Try to checkout

**Expected Result:**
- ✓ Error: "Insufficient stock for Product A"
- ✓ Redirected to cart
- ✓ Order NOT created
- ✓ Cart preserved for correction

**Pass/Fail:** _______

---

### TC-04-23: Checkout - Product Deleted
**Purpose:** Verify deleted product handled

**Precondition:** Cart has Product A

**Steps:**
1. Vendor deletes Product A
2. Buyer tries to checkout

**Expected Result:**
- ✓ Warning: "Some items no longer available"
- ✓ Product A removed from cart
- ✓ Can proceed with remaining items
- ✓ OR redirected to cart to review

**Pass/Fail:** _______

---

### TC-04-24: Stock Reduction After Checkout
**Purpose:** Verify stock accurately reduced

**Precondition:** Product has stock = 10

**Steps:**
1. Add 3 units to cart
2. Complete checkout
3. View product again

**Expected Result:**
- ✓ Stock now = 7
- ✓ Badge updates if threshold crossed
- ✓ Stock accurate in database

**Pass/Fail:** _______

---

## Test Suite: Order Confirmation

### TC-04-25: View Order Confirmation
**Purpose:** Verify confirmation page displays

**Steps:**
1. Complete checkout
2. View confirmation page

**Expected Result:**
- ✓ Success checkmark/message
- ✓ Order number shown
- ✓ Order date shown
- ✓ Total amount shown
- ✓ Items list with quantities
- ✓ Email notification message
- ✓ Links: "View All Orders", "Continue Shopping"

**Pass/Fail:** _______

---

### TC-04-26: View Order History
**Purpose:** Verify buyer can see past orders

**Precondition:** Buyer has 2 completed orders

**Steps:**
1. Go to "My Orders"

**Expected Result:**
- ✓ Shows both orders (newest first)
- ✓ Each shows: Number, Date, Status, Total
- ✓ Expandable to see items
- ✓ Can view order details

**Pass/Fail:** _______

---

### TC-04-27: Cannot View Other Buyer's Orders
**Purpose:** Verify order privacy

**Precondition:**
- Buyer1 has Order #5
- Logged in as Buyer2

**Steps:**
1. Try to access `/order/5/confirmation/` directly

**Expected Result:**
- ✓ Error: "Access denied" or 404
- ✓ Cannot view other's orders

**Pass/Fail:** _______

---

## Test Suite: Cart Badge

### TC-04-28: Cart Badge Updates
**Purpose:** Verify badge shows correct count

**Steps:**
1. Empty cart - badge shows [0] or hidden
2. Add product - badge shows [1]
3. Add 2 more of same - badge shows [3]
4. Add different product - badge shows [4]
5. Remove item - badge updates

**Expected Result:**
- ✓ Badge always accurate
- ✓ Real-time updates

**Pass/Fail:** _______

---

## Test Data Setup

**Test Products for Cart:**
```
Product A:
- Name: Laptop
- Price: R 2500
- Stock: 10

Product B:
- Name: Mouse
- Price: R 150
- Stock: 5

Product C:
- Name: Keyboard
- Price: R 450
- Stock: 0 (out of stock)
```

**Test Buyer:**
```
Username: testbuyer
Email: buyer@test.com
Password: buyer123
Group: Buyers
```

---

## Test Summary

**Total Tests:** 28
**Category:** Shopping Cart & Checkout (Buyer Feature)
**Priority:** CRITICAL (Core e-commerce functionality)
**Dependencies:**
- Authentication tests
- Product management tests

**Results:**
- Passed: ___ / 28
- Failed: ___ / 28
- Blocked: ___ / 28

---

## Notes

**Session Storage:**
- Cart stored in `request.session['cart']`
- Format: `{'product_id': quantity}`
- Timeout: 10 minutes (configurable)

**Transaction Management:**
- Checkout uses atomic transaction
- All-or-nothing operation
- Rollback on any failure

**Stock Validation:**
- Checked on add
- Checked on update
- Checked on checkout
- Prevents overselling
