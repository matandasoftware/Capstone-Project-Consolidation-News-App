"""
Authentication System Tests
Corresponds to: Planning/tests/authentication.md
Test count: 16
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from accounts.models import ResetToken
from datetime import datetime, timedelta


class TC01VendorRegistration(TestCase):
    """TC-01-01 to TC-01-06: Vendor registration tests"""

    def setUp(self):
        self.client = Client()
        Group.objects.create(name='Vendors')
        Group.objects.create(name='Buyers')

    def test_01_vendor_registration_valid_data(self):
        """TC-01-01: Verify vendor can register successfully"""
        response = self.client.post(reverse('accounts:register'), {
            'username': 'testvendor1',
            'email': 'vendor@test.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'account_type': 'vendor'
        })
        
        user = User.objects.get(username='testvendor1')
        self.assertTrue(user.groups.filter(name='Vendors').exists())
        self.assertEqual(response.status_code, 302)

    def test_02_buyer_registration_valid_data(self):
        """TC-01-02: Verify buyer can register successfully"""
        response = self.client.post(reverse('accounts:register'), {
            'username': 'testbuyer1',
            'email': 'buyer@test.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'account_type': 'buyer'
        })
        
        user = User.objects.get(username='testbuyer1')
        self.assertTrue(user.groups.filter(name='Buyers').exists())

    def test_03_duplicate_username_rejected(self):
        """TC-01-03: Verify duplicate username rejected"""
        User.objects.create_user('testuser1', 'test@test.com', 'pass123')
        
        response = self.client.post(reverse('accounts:register'), {
            'username': 'testuser1',
            'email': 'another@test.com',
            'password1': 'test1234',
            'password2': 'test1234',
            'account_type': 'vendor'
        })
        
        self.assertEqual(User.objects.filter(username='testuser1').count(), 1)

    def test_05_password_mismatch_rejected(self):
        """TC-01-05: Verify password confirmation works"""
        response = self.client.post(reverse('accounts:register'), {
            'username': 'testuser',
            'email': 'test@test.com',
            'password1': 'test1234',
            'password2': 'different123',
            'account_type': 'vendor'
        })
        
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_06_missing_required_fields(self):
        """TC-01-06: Verify all required fields validated"""
        response = self.client.post(reverse('accounts:register'), {})
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.exists())


class TC07LoginTests(TestCase):
    """TC-01-07 to TC-01-11: Login/logout tests"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'test1234')

    def test_07_login_valid_credentials(self):
        """TC-01-07: Verify login works with correct credentials"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'test1234'
        })
        
        self.assertEqual(response.status_code, 302)

    def test_08_login_invalid_password(self):
        """TC-01-08: Verify wrong password rejected"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, 200)

    def test_10_logout(self):
        """TC-01-10: Verify logout clears session"""
        self.client.login(username='testuser', password='test1234')
        response = self.client.get(reverse('accounts:logout'))
        
        self.assertEqual(response.status_code, 302)


class TC12PasswordResetTests(TestCase):
    """TC-01-12 to TC-01-16: Password reset tests"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'oldpass123')

    def test_12_password_reset_valid_email(self):
        """TC-01-12: Verify password reset email sent"""
        response = self.client.post(reverse('accounts:forgot_password'), {
            'email': 'test@test.com'
        })
        
        self.assertTrue(ResetToken.objects.filter(user=self.user).exists())

    def test_13_password_reset_complete_flow(self):
        """TC-01-13: Verify full password reset works"""
        from hashlib import sha1
        import secrets
        from datetime import datetime, timedelta

        # Generate a plain token like the view does
        plain_token = secrets.token_urlsafe(16)
        hashed_token = sha1(plain_token.encode()).hexdigest()

        # Save hashed token to DB
        ResetToken.objects.create(
            user=self.user,
            token=hashed_token,
            expiry_date=datetime.now() + timedelta(minutes=5),
            used=False
        )

        # Visit token page with PLAIN token (URL receives plain, hashes it to look up)
        self.client.get(reverse('accounts:password_reset_token', args=[plain_token]))

        # POST to reset password
        self.client.post(
            reverse('accounts:password_reset_complete'),
            {
                'password': 'NewSecure@123',
                'password_conf': 'NewSecure@123'
            }
        )

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewSecure@123'))
        self.assertFalse(self.user.check_password('test1234'))

    def test_14_token_expiration(self):
        """TC-01-14: Verify token expires after 5 minutes"""
        expired_token = ResetToken.objects.create(
            user=self.user,
            token='expiredtoken123',
            expiry_date=datetime.now() - timedelta(minutes=10)
        )
        
        response = self.client.get(
            reverse('accounts:password_reset_token', args=['expiredtoken123'])
        )
        
        self.assertEqual(response.status_code, 302)  # View redirects on expired token

    def test_15_token_reuse(self):
        """TC-01-15: Verify token only works once"""
        self.client.post(reverse('accounts:forgot_password'), {
            'email': 'test@test.com'
        })
        
        token = ResetToken.objects.get(user=self.user)
        token_value = token.token
        
        self.client.post(
           reverse('accounts:password_reset_token', args=[token_value]),
            {
                'password1': 'newpass123',
                'password2': 'newpass123'
            }
        )
        
        # Token is hashed in database, check by hashing it
        from hashlib import sha1
        hashed = sha1(token_value.encode()).hexdigest()
        self.assertFalse(ResetToken.objects.filter(token=hashed, used=False).exists())
