# 4. FAILURE HANDLING & ERROR RECOVERY

## Error Handling Approach

**Philosophy:**
1. Show user-friendly error messages
2. Prevent data corruption
3. Log errors for debugging
4. Provide recovery options

---

## Common Failure Scenarios

### 1. Authentication Errors

**Invalid Login**
- **Error:** Wrong username/password
- **Message:** "Invalid username or password. Please try again."
- **Recovery:** User can retry or use password reset

**Expired Session**
- **Error:** Session timeout (10 minutes inactive)
- **Message:** "Your session has expired. Please log in again."
- **Recovery:** Redirect to login page

**Expired Reset Token**
- **Error:** Password reset link older than 5 minutes
- **Message:** "This reset link has expired. Please request a new one."
- **Recovery:** User requests new reset email

**Unauthorized Access**
- **Error:** Buyer tries to access vendor page
- **Message:** "You must be a vendor to access this page."
- **Recovery:** Redirect to appropriate dashboard

---

### 2. Form Validation Errors

**Missing Required Fields**
- **Error:** User submits incomplete form
- **Message:** "This field is required." (shown per field)
- **Recovery:** Highlight missing fields in red

**Invalid Data**
- **Error:** Wrong data type (e.g., letters in price field)
- **Message:** "Please enter a valid number."
- **Recovery:** Show error, user corrects input

**File Upload Errors**
- **Error:** Image too large or wrong format
- **Message:** "Please upload JPG, PNG, or GIF under 5MB."
- **Recovery:** User selects correct file

---

### 3. Stock Management Errors

**Insufficient Stock**
- **Error:** User tries to order more than available
- **Message:** "Sorry, only X units available."
- **Recovery:** Cart quantity auto-adjusted to maximum
- **Prevention:** Max quantity validation on add to cart

**Product Deleted While in Cart**
- **Error:** Vendor deletes product, buyer has it in cart
- **Message:** "Some items are no longer available and were removed."
- **Recovery:** Cart automatically cleaned at checkout

**Concurrent Stock Reduction**
- **Error:** Two buyers order last item simultaneously
- **Solution:** Database check at checkout
- **Result:** First buyer succeeds, second gets "insufficient stock" error

---

### 4. Business Logic Errors

**Duplicate Review**
- **Error:** User tries to submit second review for same product
- **Message:** "You've already reviewed this product."
- **Recovery:** Redirect to edit existing review
- **Prevention:** Database unique constraint (product + user)

**Store Ownership Violation**
- **Error:** Vendor tries to edit another vendor's store
- **Message:** "Access denied. You can only edit your own stores."
- **Recovery:** Redirect to own stores
- **Prevention:** Ownership check before displaying edit form

---

### 5. Database Errors

**Connection Lost**
- **Error:** MariaDB server unavailable
- **Message:** "Database connection error. Please try again later."
- **Recovery:** Show maintenance message
- **Prevention:** Use connection pooling

**Duplicate Entry**
- **Error:** Username already exists
- **Message:** "This username is already taken."
- **Recovery:** User chooses different username
- **Prevention:** Client-side validation + database unique constraint

---

### 6. Email Errors

**Email Send Failure**
- **Error:** Cannot write email file
- **Message:** "Order placed successfully. (Email could not be sent)"
- **Recovery:** Order still created, error logged
- **Impact:** Order functional, invoice not delivered

---

## Transaction Management

### Checkout Process (Critical)
Uses Django database transactions:

```python
with transaction.atomic():
    1. Create order
    2. Create order items
    3. Reduce stock
    4. Clear cart
```

**Benefit:** If ANY step fails, ALL steps rollback
- No partial orders
- Stock stays accurate
- Cart preserved for retry

---

## User Feedback System

### Success Messages
**Format:** Green alert box
**Examples:**
- "Product added to cart!"
- "Order placed successfully!"
- "Store created!"

### Error Messages
**Format:** Red alert box
**Examples:**
- "Invalid username or password."
- "This field is required."
- "Insufficient stock."

### Warning Messages
**Format:** Orange alert box
**Examples:**
- "Some items removed due to stock."
- "Only X units available."

### Info Messages
**Format:** Blue alert box
**Examples:**
- "Invoice sent to your email."
- "Review marked as verified."

---

## Error Recovery Procedures

### Cart Recovery
- Cart stored in session (server-side)
- Survives page refresh
- Optionally persists after logout
- Lost if session expires (acceptable for capstone)

### Order Data Integrity
- All orders permanently stored
- Cannot be deleted by users
- Admin can change status only
- Order history always accessible

### Failed Checkout Recovery
- If checkout fails, cart preserved
- User can review and retry
- Stock not reduced until success
- Error message shows what went wrong

---

## Validation Rules

### Stock Validation
**When:** Add to cart, update cart, checkout
**Rule:** Requested quantity ≤ Available stock
**Failure:** Adjust to maximum, notify user

### Price Validation
**When:** Create/edit product
**Rule:** Positive decimal, maximum 10 digits
**Failure:** Show error, prevent save

### Review Validation
**When:** Submit review
**Rule:** One review per user per product
**Failure:** Redirect to edit existing review

---

## Edge Cases Handled

1. **Product Deleted in Cart:** Removed at checkout with notification
2. **Store Deactivated:** Products filtered from browsing
3. **Review After Purchase:** Auto-updates to "verified"
4. **Password Token Reuse:** Second attempt fails with error
5. **Empty Cart Checkout:** Prevented with warning message
6. **Zero Stock Purchase:** Prevented with validation

---

## Error Logging

**What is logged:**
- Database connection failures
- Email sending failures
- Unexpected exceptions
- Permission violations

**Where:**
- Development: Console output
- Production: Log files

**Purpose:**
- Debugging
- Monitoring system health
- Identifying patterns

---

## Testing Error Handling

**Scenarios Tested:**
- Submit forms with missing fields
- Try to order with insufficient stock
- Attempt unauthorized access
- Submit invalid data types
- Upload oversized files
- Use expired password reset tokens
- Delete product in someone's cart
- Concurrent order placement

---

## Future Improvements

**Planned for production:**
- Rate limiting (prevent brute force)
- Email retry logic
- Error monitoring service (Sentry)
- Automated backups
- Circuit breaker pattern
- More detailed error logs

## Error Handling Strategy

### Principles
1. **User-Friendly Messages:** Clear, actionable error messages
2. **Graceful Degradation:** System remains functional despite errors
3. **Data Integrity:** Prevent data corruption on failures
4. **Logging:** Record errors for debugging
5. **Recovery:** Provide clear paths to recover from errors

---

## Common Failure Scenarios

### 1. AUTHENTICATION FAILURES

**Invalid Login Credentials**
- **Error:** Username or password incorrect
- **Message:** "Invalid username or password. Please try again."
- **Recovery:** User can re-attempt login, use password reset
- **Prevention:** Clear form validation, helpful error message

**Expired Session**
- **Error:** User session times out (10 min inactivity)
- **Message:** "Your session has expired. Please log in again."
- **Recovery:** Redirect to login page with ?next parameter
- **Prevention:** Session timeout warning (future enhancement)

**Password Reset Token Expired**
- **Error:** Token older than 5 minutes
- **Message:** "This reset link has expired. Please request a new one."
- **Recovery:** Redirect to password reset request page
- **Prevention:** Clear expiration time in email

**Unauthorized Access Attempt**
- **Error:** User tries to access protected view
- **Message:** "You must be a [vendor/buyer] to access this page."
- **Recovery:** Redirect to login or appropriate dashboard
- **Prevention:** Hide links to unauthorized pages

---

### 2. DATABASE FAILURES

**Connection Lost**
- **Error:** MariaDB server unavailable
- **Message:** "Database connection error. Please try again later."
- **Recovery:** Retry connection, show maintenance page
- **Prevention:** Connection pooling, health checks

**Duplicate Entry**
- **Error:** Unique constraint violation (e.g., duplicate username)
- **Message:** "This username is already taken. Please choose another."
- **Recovery:** User corrects input and resubmits
- **Prevention:** Client-side validation, clear error messages

**Foreign Key Violation**
- **Error:** Referenced record doesn't exist
- **Message:** "Selected item no longer exists. Please refresh and try again."
- **Recovery:** Reload page, re-select item
- **Prevention:** Validate foreign keys before operations

**Transaction Rollback**
- **Error:** Database transaction fails mid-operation
- **Message:** "Operation failed. No changes were made."
- **Recovery:** User can retry operation
- **Prevention:** Use Django transactions for critical operations

---

### 3. FORM VALIDATION FAILURES

**Missing Required Fields**
- **Error:** User submits incomplete form
- **Message:** "This field is required." (per field)
- **Recovery:** Highlight missing fields, user completes form
- **Prevention:** Required field indicators (*), HTML5 validation

**Invalid Data Format**
- **Error:** Wrong data type (e.g., letters in price field)
- **Message:** "Please enter a valid number."
- **Recovery:** Clear invalid field, show correct format
- **Prevention:** Input type attributes, placeholder examples

**File Upload Errors**
- **Error:** File too large or wrong format
- **Message:** "Please upload JPG, PNG, or GIF images under 5MB."
- **Recovery:** User selects correct file
- **Prevention:** File size/type validation, clear instructions

---

### 4. BUSINESS LOGIC FAILURES

**Insufficient Stock**
- **Error:** User tries to order more than available
- **Message:** "Sorry, only X units available. Cart updated to maximum."
- **Recovery:** Cart quantity auto-adjusted to available stock
- **Prevention:** Real-time stock validation, max quantity limits

**Product Deleted During Checkout**
- **Error:** Product deleted while in user's cart
- **Message:** "Some items are no longer available and were removed from your cart."
- **Recovery:** Cart updated, user proceeds with remaining items
- **Prevention:** Validate cart contents before checkout

**Store Deactivated**
- **Error:** Store set to inactive while products in cart
- **Message:** "Some items from inactive stores were removed."
- **Recovery:** Cart cleaned, user notified
- **Prevention:** Filter only active store products

**Duplicate Review**
- **Error:** User tries to submit second review
- **Message:** "You've already reviewed this product. Update your existing review."
- **Recovery:** Redirect to edit review page
- **Prevention:** Database unique constraint, UI shows "Edit" instead of "Add"

---

### 5. FILE SYSTEM FAILURES

**Media Upload Failure**
- **Error:** Cannot save uploaded image
- **Message:** "Image upload failed. Please try again."
- **Recovery:** User re-uploads image
- **Prevention:** Check disk space, validate write permissions

**Email File Creation Failure**
- **Error:** Cannot write email to file (dev mode)
- **Message:** "Order placed successfully. (Email notification failed)"
- **Recovery:** Order still created, email logged as error
- **Prevention:** Ensure emails directory exists, has write permissions

---

### 6. PAYMENT FAILURES (Future)

**Note:** Payment processing not yet implemented. Plan for future:

**Payment Gateway Timeout**
- **Error:** Payment processor doesn't respond
- **Message:** "Payment processing timeout. Please check your order status."
- **Recovery:** Don't create order until payment confirmed
- **Prevention:** Implement retry logic, status checking

**Declined Payment**
- **Error:** Card declined
- **Message:** "Payment declined. Please use a different payment method."
- **Recovery:** User enters new payment details
- **Prevention:** Validate before processing

---

## Error Response Patterns

### HTTP Error Codes

**404 - Page Not Found**
- **When:** Invalid URL, deleted item
- **Message:** "Page not found. The item you're looking for doesn't exist."
- **Recovery:** Link to homepage, search functionality

**403 - Forbidden**
- **When:** Unauthorized access attempt
- **Message:** "Access denied. You don't have permission to view this page."
- **Recovery:** Redirect to appropriate dashboard

**500 - Server Error**
- **When:** Unexpected application error
- **Message:** "Something went wrong. Our team has been notified."
- **Recovery:** Link to homepage, contact support
- **Logging:** Full error logged for debugging

**400 - Bad Request**
- **When:** Invalid form submission
- **Message:** Specific field errors shown
- **Recovery:** User corrects input

---

## Transaction Management

### Critical Operations (Use Django Transactions)

**Checkout Process:**
```python
with transaction.atomic():
    # 1. Create order
    # 2. Create order items
    # 3. Reduce stock
    # 4. Clear cart
    # If ANY step fails, ALL rollback
```

**Benefits:**
- Data consistency guaranteed
- No partial orders
- Stock accurate
- All-or-nothing operation

**Failure Scenario:**
- Stock reduction fails → Entire checkout rolls back
- Order stays in cart
- User can retry

---

## Logging Strategy

### What to Log

**Errors (ERROR level):**
- Database connection failures
- Email sending failures
- Unexpected exceptions
- File system errors

**Warnings (WARNING level):**
- Insufficient stock attempts
- Invalid access attempts
- Form validation failures
- Token expiration

**Info (INFO level):**
- User registrations
- Order completions
- Store creations
- Review submissions

### Log Format
```
[TIMESTAMP] [LEVEL] [MODULE] Message
Example:
[2026-01-23 20:00:00] ERROR [product.views] Stock validation failed for product_id=5
```

### Log Storage
- Development: Console output
- Production: File-based logs, rotation enabled
- Critical errors: Email notification to admin

---

## User Feedback Mechanisms

### Success Messages
**Format:** Green alert box, checkmark icon
**Duration:** Persist until page reload
**Examples:**
- "Product added to cart!"
- "Order placed successfully!"
- "Review submitted!"

### Error Messages
**Format:** Red alert box, X icon
**Duration:** Persist until dismissed or page reload
**Examples:**
- "Invalid username or password."
- "Insufficient stock available."
- "Access denied."

### Warning Messages
**Format:** Yellow/orange alert box, warning icon
**Duration:** Persist until acknowledged
**Examples:**
- "Some items removed due to stock availability."
- "Your session will expire soon."

### Info Messages
**Format:** Blue alert box, info icon
**Duration:** Can be dismissed
**Examples:**
- "Invoice sent to your email."
- "Store set to inactive."

---

## Recovery Procedures

### Data Loss Prevention

**Cart Recovery:**
- Cart persists after logout (optional)
- Cart stored in session (server-side)
- If session expires, cart lost (acceptable for capstone)

**Order Recovery:**
- All orders permanently stored in database
- Accessible via "My Orders"
- No deletion capability (data integrity)

**User Account Recovery:**
- Password reset via email
- No account deletion (for capstone)
- Admin can deactivate accounts

### System Recovery

**Database Backup:**
- Daily automated backups (production)
- Transaction logs for point-in-time recovery
- Test restore procedure monthly

**Application Recovery:**
- Restart Django server on crashes
- Log errors for debugging
- Monitor disk space

---

## Validation Rules

### Stock Validation
**When:** Add to cart, update cart, checkout
**Rule:** Quantity ≤ Available stock
**Failure:** Adjust to maximum, notify user

### Price Validation
**When:** Product create/edit
**Rule:** Positive decimal, max 10 digits
**Failure:** Show error, require correction

### Review Validation
**When:** Submit review
**Rule:** One review per user per product
**Failure:** Redirect to edit existing review

### Store Validation
**When:** Add product
**Rule:** Store must be owned by vendor
**Failure:** Show error, prevent submission

---

## Edge Cases Handled

**1. Concurrent Stock Modifications**
- Two users order last item simultaneously
- **Solution:** Database-level stock check at checkout
- First succeeds, second gets "insufficient stock" error

**2. Product Deleted While in Cart**
- Vendor deletes product, buyer has it in cart
- **Solution:** Validate cart at checkout, remove deleted items

**3. Store Deactivated During Shopping**
- Vendor deactivates store, buyer viewing products
- **Solution:** Filter active products only, hide inactive

**4. Review After Product Purchase**
- Buyer reviews, then purchases same product
- **Solution:** Auto-update review to "verified" on next save

**5. Password Reset Token Used Twice**
- User clicks reset link twice
- **Solution:** Token deleted after first use, second attempt fails

**6. Email Delivery Failure**
- Invoice email cannot be sent
- **Solution:** Order still created, error logged, user notified

---

## Testing Error Scenarios

### Unit Tests (Future Enhancement)
- Test form validation with invalid data
- Test permission boundaries
- Test stock validation logic
- Test review verification logic

### Integration Tests
- Test checkout with insufficient stock
- Test concurrent order placement
- Test cart with deleted products

### Manual Test Cases
See separate `6_test_cases.md` document

---

## Future Improvements

**Error Monitoring:**
- Integrate Sentry or similar service
- Real-time error notifications
- Error rate tracking

**Rate Limiting:**
- Prevent brute force attacks
- API rate limits (future)
- Login attempt limits

**Circuit Breaker:**
- Temporarily disable features on repeated failures
- Prevent cascade failures

**Retry Logic:**
- Auto-retry failed email sends
- Exponential backoff for external services
