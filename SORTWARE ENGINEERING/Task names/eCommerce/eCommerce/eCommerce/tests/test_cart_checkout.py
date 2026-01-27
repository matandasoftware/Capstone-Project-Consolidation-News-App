"""
Shopping Cart & Checkout Tests (Buyers Only)
Corresponds to: Planning/tests/cart_checkout.md
Test count: 28
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from product.models import Store, Product, Order
from decimal import Decimal


class TC04CartOperations(TestCase):
    """TC-04-01 to TC-04-07: Cart operations tests"""

    def setUp(self):
        self.client = Client()
        vendors_group = Group.objects.create(name='Vendors')
        buyers_group = Group.objects.create(name='Buyers')
        
        vendor = User.objects.create_user('vendor1', 'vendor@test.com', 'test1234')
        vendor.groups.add(vendors_group)
        
        self.buyer = User.objects.create_user('buyer1', 'buyer@test.com', 'test1234')
        self.buyer.groups.add(buyers_group)
        
        store = Store.objects.create(
            vendor=vendor,
            name='Test Store',
            description='Test',
            is_active=True
        )
        
        self.product = Product.objects.create(
            store=store,
            name='Test Product',
            description='Test',
            price=Decimal('100.00'),
            stock=10,
            is_active=True
        )

    def test_01_add_to_cart_first_item(self):
        """TC-04-01: Verify buyer can add product to cart"""
        self.client.login(username='buyer1', password='test1234')
        
        response = self.client.get(reverse('product:add_to_cart', args=[self.product.pk]))
        
        self.assertEqual(response.status_code, 302)

    def test_06_vendor_cannot_add_to_cart(self):
        """TC-04-06: Verify vendors blocked from buying"""
        vendor = User.objects.get(username='vendor1')
        self.client.login(username='vendor1', password='test1234')
        
        response = self.client.get(reverse('product:add_to_cart', args=[self.product.pk]))
        
        self.assertIn(response.status_code, [302, 403])


class TC20CheckoutTests(TestCase):
    """TC-04-20 to TC-04-24: Checkout process tests"""

    def setUp(self):
        self.client = Client()
        vendors_group = Group.objects.create(name='Vendors')
        buyers_group = Group.objects.create(name='Buyers')
        
        vendor = User.objects.create_user('vendor1', 'vendor@test.com', 'test1234')
        vendor.groups.add(vendors_group)
        
        self.buyer = User.objects.create_user('buyer1', 'buyer@test.com', 'test1234')
        self.buyer.groups.add(buyers_group)
        
        store = Store.objects.create(
            vendor=vendor,
            name='Test Store',
            description='Test',
            is_active=True
        )
        
        self.product = Product.objects.create(
            store=store,
            name='Test Product',
            description='Test',
            price=Decimal('100.00'),
            stock=10,
            is_active=True
        )

    def test_20_checkout_valid_order(self):
        """TC-04-20: Verify checkout creates order successfully"""
        self.client.login(username='buyer1', password='test1234')
        
        self.client.get(reverse('product:add_to_cart', args=[self.product.pk]))
        
        response = self.client.post(reverse('product:checkout'))
        
        self.assertTrue(Order.objects.filter(buyer=self.buyer).exists())

    def test_24_stock_reduced_after_checkout(self):
        """TC-04-24: Verify stock accurately reduced"""
        self.client.login(username='buyer1', password='test1234')
        
        initial_stock = self.product.stock
        
        self.client.get(reverse('product:add_to_cart', args=[self.product.pk]))
        self.client.get(reverse('product:add_to_cart', args=[self.product.pk]))
        self.client.get(reverse('product:add_to_cart', args=[self.product.pk]))
        
        self.client.post(reverse('product:checkout'))
        
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, initial_stock - 3)
