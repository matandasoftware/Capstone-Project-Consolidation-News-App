"""
Review System Tests (Buyers Only)
Corresponds to: Planning/tests/review_system.md
Test count: 23
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from product.models import Store, Product, Order, OrderItem, Review
from decimal import Decimal


class TC05ReviewSubmission(TestCase):
    """TC-05-01 to TC-05-05: Review submission tests"""

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

    def test_01_submit_unverified_review(self):
        """TC-05-01: Verify buyer can review without purchasing"""
        self.client.login(username='buyer1', password='test1234')
        
        response = self.client.post(reverse('product:add_review', args=[self.product.pk]), {
            'rating': 4,
            'comment': 'Looks great! Planning to buy.'
        })
        
        self.assertTrue(Review.objects.filter(product=self.product, user=self.buyer).exists())
        review = Review.objects.get(product=self.product, user=self.buyer)
        self.assertFalse(review.verified)

    def test_02_submit_verified_review(self):
        """TC-05-02: Verify purchased product gets verified badge"""
        self.client.login(username='buyer1', password='test1234')
        
        order = Order.objects.create(
            buyer=self.buyer,
            total_amount=Decimal('100.00'),
            status='pending'
        )
        
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            price=self.product.price
        )
        
        response = self.client.post(reverse('product:add_review', args=[self.product.pk]), {
            'rating': 5,
            'comment': 'Excellent!'
        })
        
        review = Review.objects.get(product=self.product, user=self.buyer)
        self.assertTrue(review.verified)


class TC06EditDeleteReview(TestCase):
    """TC-05-06 to TC-05-11: Edit and delete review tests"""

    def setUp(self):
        self.client = Client()
        vendors_group = Group.objects.create(name='Vendors')
        buyers_group = Group.objects.create(name='Buyers')
        
        vendor = User.objects.create_user('vendor1', 'vendor@test.com', 'test1234')
        vendor.groups.add(vendors_group)
        
        self.buyer1 = User.objects.create_user('buyer1', 'buyer1@test.com', 'test1234')
        self.buyer1.groups.add(buyers_group)
        
        self.buyer2 = User.objects.create_user('buyer2', 'buyer2@test.com', 'test1234')
        self.buyer2.groups.add(buyers_group)
        
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

    def test_06_edit_own_review(self):
        """TC-05-06: Verify user can edit their review"""
        self.client.login(username='buyer1', password='test1234')
        
        Review.objects.create(
            product=self.product,
            user=self.buyer1,
            rating=4,
            comment='Original review',
            verified=False
        )
        
        response = self.client.post(reverse('product:add_review', args=[self.product.pk]), {
            'rating': 5,
            'comment': 'Updated review'
        })
        
        review = Review.objects.get(product=self.product, user=self.buyer1)
        self.assertEqual(review.rating, 5)

    def test_09_delete_own_review(self):
        """TC-05-09: Verify user can delete their review"""
        self.client.login(username='buyer1', password='test1234')
        
        review = Review.objects.create(
            product=self.product,
            user=self.buyer1,
            rating=4,
            comment='Test review',
            verified=False
        )
        
        response = self.client.post(reverse('product:delete_review', args=[review.pk]))
        
        self.assertFalse(Review.objects.filter(pk=review.pk).exists())

    def test_15_duplicate_review_prevented(self):
        """TC-05-15: Verify one review per user per product"""
        Review.objects.create(
            product=self.product,
            user=self.buyer1,
            rating=4,
            comment='First review',
            verified=False
        )
        
        count = Review.objects.filter(product=self.product, user=self.buyer1).count()
        self.assertEqual(count, 1)
