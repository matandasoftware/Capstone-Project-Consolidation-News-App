# Django Automated Tests

## Test Structure

All tests are organized by feature area, matching the markdown test documentation in `Planning/tests/`:

```
eCommerce/tests/
├── __init__.py
├── test_authentication.py (16 tests)
├── test_store_management.py (17 tests)
├── test_product_management.py (25 tests)
├── test_cart_checkout.py (28 tests)
├── test_review_system.py (23 tests)
└── test_security_permissions.py (30 tests)

Total: 139 automated tests
```

## Running Tests

### Run All Tests
```bash
cd eCommerce
python manage.py test
```

### Run Specific Test File
```bash
python manage.py test tests.test_authentication
python manage.py test tests.test_store_management
python manage.py test tests.test_product_management
python manage.py test tests.test_cart_checkout
python manage.py test tests.test_review_system
python manage.py test tests.test_security_permissions
```

### Run Specific Test Class
```bash
python manage.py test tests.test_authentication.TC01VendorRegistration
python manage.py test tests.test_cart_checkout.TC04CartOperations
```

### Run Specific Test Method
```bash
python manage.py test tests.test_authentication.TC01VendorRegistration.test_01_vendor_registration_valid_data
```

### Run with Verbose Output
```bash
python manage.py test --verbosity=2
```

### Keep Test Database
```bash
python manage.py test --keepdb
```

## Test Coverage

Each test file corresponds to a markdown documentation file:

| Python File | Markdown Doc | Tests | Priority |
|-------------|--------------|-------|----------|
| test_authentication.py | authentication.md | 16 | HIGH |
| test_store_management.py | store_management.md | 17 | HIGH |
| test_product_management.py | product_management.md | 25 | HIGH |
| test_cart_checkout.py | cart_checkout.md | 28 | CRITICAL |
| test_review_system.py | review_system.md | 23 | HIGH |
| test_security_permissions.py | security_permissions.md | 30 | CRITICAL |

## Test Naming Convention

Tests follow the format: `test_XX_description`

Where XX matches the test case number from the markdown documentation.

Example:
- Markdown: TC-01-01
- Python: `test_01_vendor_registration_valid_data()`

## Expected Results

All 139 tests should pass when:
- MariaDB is properly configured
- All models and views are implemented
- Permissions are correctly enforced
- Forms validate properly

## Troubleshooting

### Tests Fail with "No module named 'django'"
**Solution:** Activate virtual environment
```bash
myenv\Scripts\activate  # Windows
source myenv/bin/activate  # Linux/Mac
```

### Tests Fail with Database Errors
**Solution:** Run migrations first
```bash
python manage.py migrate
```

### Specific Test Keeps Failing
**Solution:** Check the corresponding markdown doc for manual test steps and expected behavior
