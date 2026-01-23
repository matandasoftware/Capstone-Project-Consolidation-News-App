# TEST 05: REVIEW SYSTEM (BUYERS)

## Test Suite: Submit Reviews

### TC-05-01: Submit Unverified Review
**Purpose:** Verify buyer can review without purchasing

**Precondition:**
- Logged in as buyer
- Buyer has NOT purchased Product A

**Steps:**
1. Navigate to Product A detail page
2. Click "Write a Review"
3. Fill form:
   - Rating: 4 stars
   - Comment: "Looks great! Planning to buy."
4. Click "Submit Review"

**Expected Result:**
- ✓ Review created in database
- ✓ Review shows with Yellow "Unverified" badge
- ✓ Success message shown
- ✓ Review appears on product page
- ✓ `verified = False` in database

**Pass/Fail:** _______

---

### TC-05-02: Submit Verified Review
**Purpose:** Verify purchased product gets verified badge

**Precondition:**
- Buyer purchased Product A (completed checkout)

**Steps:**
1. Go to Product A
2. Submit review (5 stars, "Excellent!")

**Expected Result:**
- ✓ Review created
- ✓ Shows Green "✓ Verified Purchase" badge
- ✓ `verified = True` in database
- ✓ Review appears at TOP of list (verified first)

**Pass/Fail:** _______

---

### TC-05-03: Review Form Validation - Missing Rating
**Purpose:** Verify rating is required

**Steps:**
1. Try to submit review without selecting rating
2. Fill comment only
3. Submit

**Expected Result:**
- ✓ Error: "This field is required" for rating
- ✓ Review not created

**Pass/Fail:** _______

---

### TC-05-04: Review Form Validation - Missing Comment
**Purpose:** Verify comment is required

**Steps:**
1. Select 5 stars
2. Leave comment empty
3. Submit

**Expected Result:**
- ✓ Error: "This field is required" for comment
- ✓ Review not created

**Pass/Fail:** _______

---

### TC-05-05: Star Rating Display
**Purpose:** Verify stars display correctly

**Steps:**
1. Submit review with 3 stars
2. View product page

**Expected Result:**
- ✓ Shows ★★★☆☆ (3 filled, 2 empty)
- ✓ Visual star representation

**Pass/Fail:** _______

---

## Test Suite: Edit Reviews

### TC-05-06: Edit Own Review
**Purpose:** Verify user can edit their review

**Precondition:** Buyer has existing review for Product A

**Steps:**
1. Go to Product A
2. Click "Write a Review" again
3. Message shown: "You already reviewed this product..."
4. Change rating from 4 to 5
5. Update comment
6. Submit

**Expected Result:**
- ✓ Review updated (not duplicated)
- ✓ New rating and comment shown
- ✓ Success: "Your review has been updated"
- ✓ Only ONE review per user per product

**Pass/Fail:** _______

---

### TC-05-07: Edit Changes to Verified After Purchase
**Purpose:** Verify verification auto-updates

**Precondition:**
- Buyer left unverified review
- Buyer then purchases product

**Steps:**
1. View product (after purchase)
2. Edit review (any change)
3. Save

**Expected Result:**
- ✓ Review now shows "Verified" badge
- ✓ Auto-check: OrderItem exists for this buyer + product
- ✓ `verified = True` in database

**Pass/Fail:** _______

---

### TC-05-08: Cannot Edit Other's Review
**Purpose:** Verify ownership enforced

**Precondition:**
- Buyer1 has review for Product A
- Logged in as Buyer2

**Steps:**
1. View Product A as Buyer2
2. Look for Buyer1's review

**Expected Result:**
- ✓ Edit/Delete buttons NOT visible on Buyer1's review
- ✓ Can only edit own reviews
- ✓ Direct URL access blocked

**Pass/Fail:** _______

---

## Test Suite: Delete Reviews

### TC-05-09: Delete Own Review
**Purpose:** Verify user can delete their review

**Precondition:** Buyer has review for Product A

**Steps:**
1. View Product A
2. Click "Delete" on own review
3. Confirmation page appears
4. Shows review details (rating, comment, date)
5. Click "Yes, Delete Review"

**Expected Result:**
- ✓ Review deleted from database
- ✓ Success: "Your review has been deleted"
- ✓ Review no longer on product page
- ✓ Can submit new review later

**Pass/Fail:** _______

---

### TC-05-10: Delete - Cancel
**Purpose:** Verify cancel preserves review

**Steps:**
1. Click "Delete"
2. View confirmation
3. Click "Cancel"

**Expected Result:**
- ✓ Review NOT deleted
- ✓ Redirected to product page
- ✓ Review still visible

**Pass/Fail:** _______

---

### TC-05-11: Cannot Delete Other's Review
**Purpose:** Verify ownership enforced

**Steps:**
1. As Buyer2, try to delete Buyer1's review (direct URL)

**Expected Result:**
- ✓ Error: 404 or "Access denied"
- ✓ Review not deleted

**Pass/Fail:** _______

---

## Test Suite: Review Display

### TC-05-12: Reviews Sorted - Verified First
**Purpose:** Verify verified reviews appear first

**Precondition:** Product has 2 verified + 2 unverified reviews

**Steps:**
1. View product detail page

**Expected Result:**
- ✓ Verified reviews at top
- ✓ Then unverified reviews
- ✓ Within each group, newest first

**Pass/Fail:** _______

---

### TC-05-13: Review Shows Reviewer Username
**Purpose:** Verify attribution

**Steps:**
1. View product with reviews

**Expected Result:**
- ✓ Each review shows username
- ✓ Date posted shown
- ✓ Rating shown
- ✓ Comment shown

**Pass/Fail:** _______

---

### TC-05-14: Product with No Reviews
**Purpose:** Verify empty state

**Precondition:** Product has 0 reviews

**Steps:**
1. View product detail

**Expected Result:**
- ✓ Message: "No reviews yet. Be the first to review!"
- ✓ "Write a Review" button visible (for buyers)

**Pass/Fail:** _______

---

## Test Suite: Duplicate Review Prevention

### TC-05-15: Cannot Submit Duplicate Review
**Purpose:** Verify one review per user per product

**Precondition:** Buyer already reviewed Product A

**Steps:**
1. Try to access add review URL directly
2. Or click "Write a Review"

**Expected Result:**
- ✓ Redirected to edit form
- ✓ Message: "You already reviewed this product"
- ✓ Existing review loaded for editing
- ✓ Database constraint prevents duplicate

**Pass/Fail:** _______

---

### TC-05-16: Can Review Different Products
**Purpose:** Verify user can review multiple products

**Steps:**
1. Submit review for Product A
2. Submit review for Product B
3. Submit review for Product C

**Expected Result:**
- ✓ All three reviews created
- ✓ No conflicts
- ✓ Each tracked separately

**Pass/Fail:** _______

---

## Test Suite: Verification Logic

### TC-05-17: Auto-Verification on Save
**Purpose:** Verify verification checked automatically

**Steps:**
1. Buyer purchases Product A
2. Buyer submits review for Product A

**Expected Result:**
- ✓ System checks OrderItem table
- ✓ Finds order with this buyer + product
- ✓ Sets `verified = True`
- ✓ No manual verification needed

**Pass/Fail:** _______

---

### TC-05-18: Verification Persists After Order
**Purpose:** Verify verified status permanent

**Precondition:** Buyer left verified review

**Steps:**
1. Admin changes order status
2. View review again

**Expected Result:**
- ✓ Review still shows "Verified"
- ✓ Status doesn't change
- ✓ Based on purchase history, not order status

**Pass/Fail:** _______

---

## Test Suite: Permissions

### TC-05-19: Vendor Cannot Leave Review
**Purpose:** Verify vendors blocked from reviewing

**Precondition:** Logged in as vendor

**Steps:**
1. View product detail

**Expected Result:**
- ✓ "Write a Review" button NOT visible
- ✓ Direct URL access blocked
- ✓ Error if attempted

**Pass/Fail:** _______

---

### TC-05-20: Anonymous Cannot Leave Review
**Purpose:** Verify login required

**Precondition:** Not logged in

**Steps:**
1. View product
2. Try to access review form

**Expected Result:**
- ✓ "Write a Review" button hidden OR
- ✓ Message: "Login as buyer to leave review"
- ✓ Redirected to login if URL accessed

**Pass/Fail:** _______

---

### TC-05-21: Buyer Can Review Own Product
**Purpose:** Verify buyer can review if they purchased (even if vendor too)

**Precondition:** User is both vendor AND buyer

**Steps:**
1. As buyer, purchase product
2. Leave review

**Expected Result:**
- ✓ Review allowed
- ✓ Shows as verified
- ✓ Based on buyer role

**Pass/Fail:** _______

---

## Test Suite: Review Statistics

### TC-05-22: Product Shows Review Count
**Purpose:** Verify review count displayed

**Precondition:** Product has 5 reviews

**Steps:**
1. View product

**Expected Result:**
- ✓ Shows "5 reviews" or "(5)"
- ✓ Count accurate
- ✓ Updates when reviews added/deleted

**Pass/Fail:** _______

---

### TC-05-23: Average Rating Display (Optional)
**Purpose:** Verify average rating calculated

**Precondition:** Product has reviews: 5★, 4★, 3★

**Steps:**
1. View product

**Expected Result:**
- ✓ Shows average: 4.0★ (if implemented)
- ✓ OR shows all ratings
- ✓ Accurate calculation

**Pass/Fail:** _______ (Optional feature)

---

## Test Data Setup

**Test Products:**
```
Product A:
- Name: Laptop
- Has 3 reviews (2 verified, 1 unverified)

Product B:
- Name: Mouse
- Has 0 reviews
```

**Test Buyers:**
```
Buyer1 (purchased Product A):
- Username: buyer1
- Can leave verified review

Buyer2 (NOT purchased):
- Username: buyer2
- Can only leave unverified review
```

---

## Test Summary

**Total Tests:** 23
**Category:** Review System (Buyer Feature)
**Priority:** HIGH
**Dependencies:**
- Authentication tests
- Product management tests
- Cart & checkout tests (for verified reviews)

**Results:**
- Passed: ___ / 23
- Failed: ___ / 23
- Blocked: ___ / 23

---

## Notes

**Verification Logic:**
```python
has_purchased = OrderItem.objects.filter(
    order__buyer=user,
    product=product
).exists()
review.verified = has_purchased
```

**Database Constraint:**
- UNIQUE(product_id, user_id)
- Prevents duplicate reviews
- One review per user per product

**Display Order:**
- Verified reviews first
- Then by date (newest first)
- Within each group
