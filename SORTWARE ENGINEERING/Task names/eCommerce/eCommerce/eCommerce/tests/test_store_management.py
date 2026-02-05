"""
Store Management Tests (Vendors Only)
Corresponds to: Planning/tests/store_management.md
Test count: 17
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from product.models import Store, Product


class TC02StoreCreation(TestCase):
    """TC-02-01 to TC-02-03: Store creation tests"""

    def setUp(self):
        self.client = Client()
        vendors_group = Group.objects.create(name='Vendors')
        
        self.vendor = User.objects.create_user('vendor1', 'vendor@test.com', 'test1234')
        self.vendor.groups.add(vendors_group)

    def test_01_create_store_valid_data(self):
        """TC-02-01: Verify vendor can create store"""
        self.client.login(username='vendor1', password='test1234')
        
        response = self.client.post(reverse('product:store_create'), {
            'name': 'Electronics Hub',
            'description': 'Quality electronics',
            'is_active': True
        })
        
        self.assertTrue(Store.objects.filter(name='Electronics Hub').exists())
        store = Store.objects.get(name='Electronics Hub')
        self.assertEqual(store.vendor, self.vendor)

    def test_02_create_store_missing_name(self):
        """TC-02-02: Verify name is required"""
        self.client.login(username='vendor1', password='test1234')
        
        response = self.client.post(reverse('product:store_create'), {
            'description': 'Test description'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Store.objects.exists())

    def test_03_create_store_inactive(self):
        """TC-02-03: Verify store can be created inactive"""
        self.client.login(username='vendor1', password='test1234')
        
        # Checkboxes: unchecked = omit field, checked = any value
        response = self.client.post(reverse('product:store_create'), {
            'name': 'Test Store',
            'description': 'Test'
            # is_active omitted = False (unchecked)
        })
        store = Store.objects.get(name='Test Store')
        self.assertFalse(store.is_active)


class TC04ViewEditDeleteStore(TestCase):
    """TC-02-04 to TC-02-10: Store CRUD operations"""

    def setUp(self):
        self.client = Client()
        vendors_group = Group.objects.create(name='Vendors')
        
        self.vendor1 = User.objects.create_user('vendor1', 'v1@test.com', 'test1234')
        self.vendor1.groups.add(vendors_group)
        
        self.vendor2 = User.objects.create_user('vendor2', 'v2@test.com', 'test1234')
        self.vendor2.groups.add(vendors_group)
        
        self.store1 = Store.objects.create(
            vendor=self.vendor1,
            name='Store1',
            description='Test',
            is_active=True
        )
        
        self.store2 = Store.objects.create(
            vendor=self.vendor2,
            name='Store2',
            description='Test',
            is_active=True
        )

    def test_04_view_store_list(self):
        """TC-02-04: Verify vendor sees only their stores"""
        self.client.login(username='vendor1', password='test1234')
        
        response = self.client.get(reverse('product:store_list'))
        
        self.assertContains(response, 'Store1')
        self.assertNotContains(response, 'Store2')

    def test_06_edit_store_update_name(self):
        """TC-02-06: Verify store can be edited"""
        self.client.login(username='vendor1', password='test1234')
        
        response = self.client.post(reverse('product:store_update', args=[self.store1.pk]), {
            'name': 'Updated Store',
            'description': 'Updated',
            'is_active': True
        })
        
        self.store1.refresh_from_db()
        self.assertEqual(self.store1.name, 'Updated Store')

    def test_07_toggle_active_status(self):
        """TC-02-07: Verify active status can be changed"""
        self.client.login(username='vendor1', password='test1234')
        
        # Checkboxes: unchecked = omit field
        self.client.post(reverse('product:store_update', args=[self.store1.pk]), {
            'name': 'Store1',
            'description': self.store1.description
            # is_active omitted = False (unchecked)
        })
        
        self.store1.refresh_from_db()
        self.assertFalse(self.store1.is_active)

    def test_09_delete_store_confirmed(self):
        """TC-02-09: Verify store can be deleted"""
        self.client.login(username='vendor1', password='test1234')
        
        response = self.client.post(reverse('product:store_delete', args=[self.store1.pk]))
        
        self.assertFalse(Store.objects.filter(pk=self.store1.pk).exists())


class TC11StorePermissions(TestCase):
    """TC-02-11 to TC-02-14: Store ownership and permissions"""

    def setUp(self):
        self.client = Client()
        vendors_group = Group.objects.create(name='Vendors')
        buyers_group = Group.objects.create(name='Buyers')
        
        self.vendor1 = User.objects.create_user('vendor1', 'v1@test.com', 'test1234')
        self.vendor1.groups.add(vendors_group)
        
        self.vendor2 = User.objects.create_user('vendor2', 'v2@test.com', 'test1234')
        self.vendor2.groups.add(vendors_group)
        
        self.buyer = User.objects.create_user('buyer1', 'buyer@test.com', 'test1234')
        self.buyer.groups.add(buyers_group)
        
        self.store = Store.objects.create(
            vendor=self.vendor1,
            name='Store1',
            description='Test',
            is_active=True
        )

    def test_11_buyer_cannot_create_store(self):
        """TC-02-11: Verify buyers blocked from vendor features"""
        self.client.login(username='buyer1', password='test1234')
        
        response = self.client.get(reverse('product:store_create'))
        
        self.assertIn(response.status_code, [302, 403])

    def test_12_cannot_edit_other_vendor_store(self):
        """TC-02-12: Verify store ownership enforced"""
        self.client.login(username='vendor2', password='test1234')
        
        response = self.client.get(reverse('product:store_update', args=[self.store.pk]))
        
        self.assertIn(response.status_code, [302, 403, 404])

    def test_13_cannot_delete_other_vendor_store(self):
        """TC-02-13: Verify delete ownership enforced"""
        self.client.login(username='vendor2', password='test1234')
        
        response = self.client.post(reverse('product:store_delete', args=[self.store.pk]))
        
        self.assertTrue(Store.objects.filter(pk=self.store.pk).exists())

    def test_14_anonymous_cannot_access_stores(self):
        """TC-02-14: Verify login required"""
        response = self.client.get(reverse('product:store_list'))
        
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)


class TC15StoreProductRelationship(TestCase):
    """TC-02-15 to TC-02-17: Store-product relationship tests"""

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

    def test_16_delete_store_deletes_products(self):
        """TC-02-16: Verify cascade deletion"""
        Product.objects.create(
            store=self.store,
            name='Product1',
            description='Test',
            price=100.00,
            stock=10,
            is_active=True
        )
        
        Product.objects.create(
            store=self.store,
            name='Product2',
            description='Test',
            price=50.00,
            stock=5,
            is_active=True
        )
        
        self.client.login(username='vendor1', password='test1234')
        self.client.post(reverse('product:store_delete', args=[self.store.pk]))
        
        self.assertEqual(Product.objects.filter(store=self.store).count(), 0)
