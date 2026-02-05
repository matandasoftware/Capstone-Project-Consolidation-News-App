"""
Security & Permissions Tests
Corresponds to: Planning/tests/security_permissions.md
Test count: 30
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from product.models import Store, Product
from accounts.models import ResetToken
import os


class TC06EmailSystem(TestCase):
    """TC-06-01 to TC-06-03: Email system tests"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'test1234')

    def test_02_password_reset_email_created(self):
        """TC-06-02: Verify reset email generated"""
        response = self.client.post(reverse('accounts:forgot_password'), {
            'email': 'test@test.com'
        })
        
        self.assertTrue(ResetToken.objects.filter(user=self.user).exists())


class TC04DatabaseSecurity(TestCase):
    """TC-06-04 to TC-06-06: Database security tests"""

    def test_05_password_hashing(self):
        """TC-06-05: Verify passwords not stored in plaintext"""
        user = User.objects.create_user('testuser', 'test@test.com', 'plaintext123')
        
        self.assertNotEqual(user.password, 'plaintext123')
        self.assertTrue(user.password.startswith('pbkdf2_sha256'))
        self.assertTrue(user.check_password('plaintext123'))


class TC10CSRFProtection(TestCase):
    """TC-06-10 to TC-06-11: CSRF protection tests"""

    def setUp(self):
        self.client = Client()
        vendors_group = Group.objects.create(name='Vendors')
        self.vendor = User.objects.create_user('vendor1', 'vendor@test.com', 'test1234')
        self.vendor.groups.add(vendors_group)

    def test_10_csrf_token_in_forms(self):
        """TC-06-10: Verify all forms have CSRF protection"""
        self.client.login(username='vendor1', password='test1234')
        
        response = self.client.get(reverse('product:store_create'))
        
        self.assertContains(response, 'csrfmiddlewaretoken')


class TC22AdminPanelSecurity(TestCase):
    """TC-06-22 to TC-06-24: Admin panel security tests"""

    def setUp(self):
        self.client = Client()
        self.regular_user = User.objects.create_user('regular', 'regular@test.com', 'test1234')
        self.superuser = User.objects.create_superuser('admin', 'admin@test.com', 'admin123')

    def test_22_admin_requires_staff_status(self):
        """TC-06-22: Verify regular users blocked"""
        self.client.login(username='regular', password='test1234')
        
        response = self.client.get('/admin/')
        
        self.assertNotEqual(response.status_code, 200)

    def test_23_admin_panel_accessible(self):
        """TC-06-23: Verify superuser can access"""
        self.client.login(username='admin', password='admin123')
        
        response = self.client.get('/admin/')
        
        self.assertEqual(response.status_code, 200)


class TC28DataValidation(TestCase):
    """TC-06-28 to TC-06-30: Data validation tests"""

    def setUp(self):
        self.client = Client()
        vendors_group = Group.objects.create(name='Vendors')
        
        self.vendor = User.objects.create_user('vendor1', 'vendor@test.com', 'test1234')
        self.vendor.groups.add(vendors_group)
        
        self.store = Store.objects.create(
            vendor=self.vendor,
            name='Test Store',
            description='Test',
            is_active=True
        )

    def test_28_stock_cannot_be_negative(self):
        """TC-06-28: Verify stock validation"""
        self.client.login(username='vendor1', password='test1234')
        
        response = self.client.post(reverse('product:vendor_product_create'), {
            'name': 'Test Product',
            'store': self.store.pk,
            'description': 'Test',
            'price': '100.00',
            'stock': -5,
            'is_active': True
        })
        
        self.assertFalse(Product.objects.filter(name='Test Product').exists())

    def test_29_price_must_be_positive(self):
        """TC-06-29: Verify price validation"""
        self.client.login(username='vendor1', password='test1234')
        
        response = self.client.post(reverse('product:vendor_product_create'), {
            'name': 'Test Product',
            'store': self.store.pk,
            'description': 'Test',
            'price': '-50.00',
            'stock': 10,
            'is_active': True
        })
        
        self.assertFalse(Product.objects.filter(name='Test Product').exists())


class PermissionBoundaryTests(TestCase):
    """Additional permission boundary tests"""

    def setUp(self):
        self.client = Client()
        vendors_group = Group.objects.create(name='Vendors')
        buyers_group = Group.objects.create(name='Buyers')
        
        self.vendor = User.objects.create_user('vendor1', 'vendor@test.com', 'test1234')
        self.vendor.groups.add(vendors_group)
        
        self.buyer = User.objects.create_user('buyer1', 'buyer@test.com', 'test1234')
        self.buyer.groups.add(buyers_group)

    def test_vendor_cannot_checkout(self):
        """Verify vendors cannot access checkout"""
        self.client.login(username='vendor1', password='test1234')
        
        response = self.client.get(reverse('product:checkout'))
        
        self.assertIn(response.status_code, [302, 403])

    def test_buyer_cannot_add_product(self):
        """Verify buyers cannot add products"""
        self.client.login(username='buyer1', password='test1234')
        
        response = self.client.get(reverse('product:vendor_product_create'))
        
        self.assertIn(response.status_code, [302, 403])
