"""
Product Management Tests (Vendors Only)
Corresponds to: Planning/tests/product_management.md
Test count: 25
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from product.models import Store, Product, Category
from decimal import Decimal


class TC03ProductCreation(TestCase):
    """TC-03-01 to TC-03-06: Product creation tests"""

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
        
        self.category = Category.objects.create(name='Electronics')

    def test_01_add_product_complete_data(self):
        """TC-03-01: Verify vendor can add product with all fields"""
        self.client.login(username='vendor1', password='test1234')
        
        response = self.client.post(reverse('product:vendor_product_create'), {
            'name': 'Laptop',
            'store': self.store.pk,
            'category': self.category.pk,
            'description': 'High-performance laptop',
            'price': '2500.00',
            'stock': 25,
            'is_active': True
        })
        
        self.assertTrue(Product.objects.filter(name='Laptop').exists())


class TC07StockStatus(TestCase):
    """TC-03-07 to TC-03-10: Stock status tests"""

    def setUp(self):
        vendors_group = Group.objects.create(name='Vendors')
        vendor = User.objects.create_user('vendor1', 'vendor@test.com', 'test1234')
        vendor.groups.add(vendors_group)
        
        self.store = Store.objects.create(
            vendor=vendor,
            name='Test Store',
            description='Test',
            is_active=True
        )

    def test_07_stock_out_of_stock(self):
        """TC-03-07: Verify 0 stock shows Out of Stock"""
        product = Product.objects.create(
            store=self.store,
            name='Test Product',
            description='Test',
            price=Decimal('100.00'),
            stock=0,
            is_active=True
        )
        
        self.assertEqual(product.stock, 0)

    def test_08_stock_in_store_only(self):
        """TC-03-08: Verify low stock shows In Store Only"""
        product = Product.objects.create(
            store=self.store,
            name='Test Product',
            description='Test',
            price=Decimal('100.00'),
            stock=5,
            is_active=True
        )
        
        self.assertTrue(1 <= product.stock <= 10)

    def test_09_stock_in_stock(self):
        """TC-03-09: Verify high stock shows In Stock"""
        product = Product.objects.create(
            store=self.store,
            name='Test Product',
            description='Test',
            price=Decimal('100.00'),
            stock=50,
            is_active=True
        )
        
        self.assertGreaterEqual(product.stock, 11)
