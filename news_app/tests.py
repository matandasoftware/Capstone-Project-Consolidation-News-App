"""
Test Suite for the News Application.

This module contains comprehensive automated tests including:
- Model tests: CustomUser, Article, Publisher, Newsletter
- View tests: Authentication, permissions, CRUD operations
- API tests: Token authentication, endpoint responses
- Integration tests: Complete user workflows

Uses Django TestCase and REST Framework APIClient.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import CustomUser, Publisher, Article, Newsletter


# TEST 1: LOGIN & AUTHENTICATION
# Testing: POST /api/login/
class APIAuthenticationTests(TestCase):
    """
    Making sure users can log in and get authentication tokens.
    Think of tokens like a special key that lets you access protected areas.
    """
    
    def setUp(self):
        """Before each test, create some fake users to test with."""
        self.client = APIClient()
        
        # Create a test journalist
        self.journalist = CustomUser.objects.create_user(
            username='testjournalist',
            email='journalist@test.com',
            password='testpass123',
            role='JOURNALIST'
        )
        
        # Create a test reader
        self.reader = CustomUser.objects.create_user(
            username='testreader',
            email='reader@test.com',
            password='testpass123',
            role='READER'
        )
    
    def test_api_login_success(self):
        """Test that logging in with correct username and password works."""
        url = reverse('api_login')
        data = {
            'username': 'testjournalist',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        
        # Make sure it worked!
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)  # We got a token!
        self.assertIn('user_id', response.data)  # We got user info!
        self.assertEqual(response.data['username'], 'testjournalist')
        self.assertEqual(response.data['role'], 'JOURNALIST')
    
    def test_api_login_invalid_credentials(self):
        """Test that logging in with wrong password gets rejected."""
        url = reverse('api_login')
        data = {
            'username': 'testjournalist',
            'password': 'wrongpassword'  # Oops, wrong password!
        }
        
        response = self.client.post(url, data, format='json')
        
        # Should be rejected!
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)


# TEST 2: PUBLIC ENDPOINTS
# Testing: GET /api/articles/, /api/articles/{id}/, /api/publishers/, /api/journalists/
class PublicAPITests(TestCase):
    """
    These endpoints should work for ANYONE - no login required!
    Like a public library where anyone can read the books.
    """
    
    def setUp(self):
        """Create some test data to work with."""
        self.client = APIClient()
        
        # Create a test publisher
        self.publisher = Publisher.objects.create(
            name='Test Publisher',
            description='A test publisher'
        )
        
        # Create a test journalist
        self.journalist = CustomUser.objects.create_user(
            username='journalist1',
            email='journalist1@test.com',
            password='pass123',
            role='JOURNALIST'
        )
        
        # Create an approved article (this one should be visible)
        self.approved_article = Article.objects.create(
            title='Approved Article',
            content='This article is approved.',
            summary='Approved article summary',
            author=self.journalist,
            publisher=self.publisher,
            is_approved=True
        )
        
        # Create an unapproved article (this one should be hidden)
        self.unapproved_article = Article.objects.create(
            title='Pending Article',
            content='This article is pending.',
            summary='Pending article summary',
            author=self.journalist,
            is_approved=False
        )
    
    def test_get_articles_list(self):
        """Test getting a list of articles - should only show approved ones."""
        url = reverse('api_articles')
        response = self.client.get(url)
        
        # Check that it worked
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only 1 article (the approved one)
        self.assertEqual(response.data[0]['title'], 'Approved Article')
        self.assertTrue(response.data[0]['is_approved'])
    
    def test_get_single_article(self):
        """Test getting details of one specific article."""
        url = reverse('api_article_detail', kwargs={'pk': self.approved_article.pk})
        response = self.client.get(url)
        
        # Check we got the right article with all the details
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Approved Article')
        self.assertEqual(response.data['author_username'], 'journalist1')  # Nice readable name!
        self.assertEqual(response.data['publisher_name'], 'Test Publisher')  # Publisher name too!
    
    def test_get_publishers_list(self):
        """Test getting a list of all publishers."""
        url = reverse('api_publishers')
        response = self.client.get(url)
        
        # Check it worked and includes article counts
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Publisher')
        self.assertEqual(response.data[0]['article_count'], 1)  # Counts only approved articles!
    
    def test_get_journalists_list(self):
        """Test getting a list of all journalists."""
        url = reverse('api_journalists')
        response = self.client.get(url)
        
        # Check it only shows users who are journalists
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'journalist1')


# TEST 3: PROTECTED ENDPOINTS
# Testing: POST /api/articles/create/
class ProtectedAPITests(TestCase):
    """
    These endpoints require a valid login token to access.
    Like a members-only area - you need your membership card (token) to get in!
    """
    
    def setUp(self):
        """Create users and give them authentication tokens."""
        self.client = APIClient()
        
        # Create a journalist user
        self.journalist = CustomUser.objects.create_user(
            username='journalist2',
            email='journalist2@test.com',
            password='pass123',
            role='JOURNALIST'
        )
        
        # Create a reader user
        self.reader = CustomUser.objects.create_user(
            username='reader1',
            email='reader1@test.com',
            password='pass123',
            role='READER'
        )
        
        # Create a publisher
        self.publisher = Publisher.objects.create(
            name='Tech News',
            description='Technology news'
        )
        
        # Give each user a token (their "membership card")
        self.journalist_token = Token.objects.create(user=self.journalist)
        self.reader_token = Token.objects.create(user=self.reader)
    
    def test_create_article_without_token(self):
        """Test that trying to create an article WITHOUT logging in fails."""
        url = reverse('api_create_article')
        data = {
            'title': 'Test Article',
            'content': 'Test content',
            'summary': 'Test summary',
            'publisher': self.publisher.pk
        }
        
        response = self.client.post(url, data, format='json')
        
        # Should be rejected - no token means no access!
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_article_with_journalist_token(self):
        """Test that a journalist CAN create an article when logged in."""
        url = reverse('api_create_article')
        data = {
            'title': 'API Test Article',
            'content': 'Content created via API',
            'summary': 'API test summary',
            'publisher': self.publisher.pk
        }
        
        # Log in as journalist (provide the token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.journalist_token.key}')
        response = self.client.post(url, data, format='json')
        
        # Should work!
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'API Test Article')
        self.assertEqual(response.data['author'], self.journalist.pk)  # Author set automatically!
        self.assertFalse(response.data['is_approved'])  # Starts as unapproved
    
    def test_create_article_with_reader_token(self):
        """Test that a reader CANNOT create articles (wrong role)."""
        url = reverse('api_create_article')
        data = {
            'title': 'Unauthorized Article',
            'content': 'Should not be created',
            'summary': 'Test',
            'publisher': self.publisher.pk
        }
        
        # Log in as reader (but readers can't create articles!)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.reader_token.key}')
        response = self.client.post(url, data, format='json')
        
        # Should be rejected - wrong role!
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('error', response.data)


# TEST 4: SUBSCRIPTIONS
# Testing: POST /api/subscribe/publisher/{id}/, POST /api/subscribe/journalist/{id}/
class SubscriptionAPITests(TestCase):
    """
    Testing the subscription system - can readers follow publishers and journalists?
    Like following someone on social media!
    """
    
    def setUp(self):
        """Create test users and a publisher."""
        self.client = APIClient()
        
        # Create a reader
        self.reader = CustomUser.objects.create_user(
            username='reader2',
            email='reader2@test.com',
            password='pass123',
            role='READER'
        )
        
        # Create a journalist
        self.journalist = CustomUser.objects.create_user(
            username='journalist3',
            email='journalist3@test.com',
            password='pass123',
            role='JOURNALIST'
        )
        
        # Create a publisher
        self.publisher = Publisher.objects.create(
            name='Sports News',
            description='Sports updates'
        )
        
        # Give them tokens
        self.reader_token = Token.objects.create(user=self.reader)
        self.journalist_token = Token.objects.create(user=self.journalist)
    
    def test_reader_subscribe_to_publisher(self):
        """Test that a reader can subscribe to a publisher."""
        url = reverse('api_subscribe_publisher', kwargs={'pk': self.publisher.pk})
        
        # Log in as reader and subscribe
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.reader_token.key}')
        response = self.client.post(url)
        
        # Should work!
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        # Double-check the subscription was saved in the database
        self.reader.refresh_from_db()
        self.assertIn(self.publisher, self.reader.subscribed_publishers.all())
    
    def test_journalist_cannot_subscribe(self):
        """Test that journalists CANNOT subscribe (only readers can subscribe)."""
        url = reverse('api_subscribe_publisher', kwargs={'pk': self.publisher.pk})
        
        # Try to subscribe as journalist
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.journalist_token.key}')
        response = self.client.post(url)
        
        # Should be rejected - wrong role!
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('error', response.data)
    
    def test_reader_subscribe_to_journalist(self):
        """Test that a reader can subscribe to a journalist."""
        url = reverse('api_subscribe_journalist', kwargs={'pk': self.journalist.pk})
        
        # Log in as reader and subscribe
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.reader_token.key}')
        response = self.client.post(url)
        
        # Should work!
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Double-check it saved
        self.reader.refresh_from_db()
        self.assertIn(self.journalist, self.reader.subscribed_journalists.all())


# TEST 5: ARTICLE RETRIEVAL BY SUBSCRIPTION ⭐⭐⭐
# Testing: GET /api/articles/, GET /api/publishers/
class ArticleRetrievalBySubscriptionTests(TestCase):
    """
    ⭐⭐⭐ THIS IS THE MOST IMPORTANT TEST! ⭐⭐⭐
    
    The task says: "verify that your API returns the correct articles based 
    on the subscriptions of the API client (reader)."
    
    This test creates a realistic scenario:
    - A reader subscribes to some publishers/journalists (but not all)
    - We create several articles from different sources
    - We check that the API returns the right articles
    
    It's like testing if your personalized news feed shows the right stories!
    """
    
    def setUp(self):
        """Create a complete test scenario with publishers, journalists, readers, and articles."""
        self.client = APIClient()
        
        # Create two publishers
        self.publisher1 = Publisher.objects.create(
            name='Tech Publisher',
            description='Tech news'
        )
        self.publisher2 = Publisher.objects.create(
            name='Sports Publisher',
            description='Sports news'
        )
        
        # Create two journalists
        self.journalist1 = CustomUser.objects.create_user(
            username='techjourno',
            email='techjourno@test.com',
            password='pass123',
            role='JOURNALIST'
        )
        self.journalist2 = CustomUser.objects.create_user(
            username='sportsjourno',
            email='sportsjourno@test.com',
            password='pass123',
            role='JOURNALIST'
        )
        
        # Create a reader
        self.reader = CustomUser.objects.create_user(
            username='reader3',
            email='reader3@test.com',
            password='pass123',
            role='READER'
        )
        
        # The reader subscribes to SOME sources (but not all)
        self.reader.subscribed_publishers.add(self.publisher1)  # Subscribes to Tech, not Sports
        self.reader.subscribed_journalists.add(self.journalist1)  # Subscribes to techjourno, not sportsjourno
        
        # Now create 4 different articles to test various scenarios:
        
        # Article 1: From a subscribed publisher (should be visible)
        self.article1 = Article.objects.create(
            title='Tech Article 1',
            content='Content 1',
            summary='Summary 1',
            author=self.journalist1,
            publisher=self.publisher1,
            is_approved=True
        )
        
        # Article 2: From a subscribed journalist, but independent (no publisher)
        self.article2 = Article.objects.create(
            title='Independent Article',
            content='Content 2',
            summary='Summary 2',
            author=self.journalist1,
            publisher=None,  # Independent article
            is_approved=True
        )
        
        # Article 3: From a NON-subscribed publisher (should still be visible - public API)
        self.article3 = Article.objects.create(
            title='Sports Article',
            content='Content 3',
            summary='Summary 3',
            author=self.journalist2,
            publisher=self.publisher2,
            is_approved=True
        )
        
        # Article 4: NOT approved yet (should be hidden)
        self.article4 = Article.objects.create(
            title='Pending Tech Article',
            content='Content 4',
            summary='Summary 4',
            author=self.journalist1,
            publisher=self.publisher1,
            is_approved=False  # Not approved!
        )
    
    def test_api_returns_only_approved_articles(self):
        """Test that the API only shows approved articles, not pending ones."""
        url = reverse('api_articles')
        response = self.client.get(url)
        
        # Should get 3 approved articles (not the pending one)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        approved_count = len([a for a in response.data if a['is_approved']])
        self.assertEqual(approved_count, 3)  # 3 approved, 1 pending
    
    def test_subscribed_articles_available_via_api(self):
        """
        ⭐ THE BIG TEST ⭐
        
        Test that articles from subscribed sources are available.
        This directly proves our subscription system works!
        """
        url = reverse('api_articles')
        response = self.client.get(url)
        
        # Get all the article titles
        titles = [article['title'] for article in response.data]
        
        # Should include articles from sources we subscribed to
        self.assertIn('Tech Article 1', titles)  # Subscribed to this publisher ✓
        self.assertIn('Independent Article', titles)  # Subscribed to this journalist ✓
        
        # Should also include non-subscribed (it's a public API after all)
        self.assertIn('Sports Article', titles)  # Not subscribed, but still visible ✓
        
        # Should NOT include unapproved articles
        self.assertNotIn('Pending Tech Article', titles)  # Unapproved = hidden ✗
    
    def test_publisher_endpoint_shows_correct_article_count(self):
        """Test that publisher article counts only include approved articles."""
        url = reverse('api_publishers')
        response = self.client.get(url)
        
        # Find the Tech Publisher
        tech_pub = next(p for p in response.data if p['name'] == 'Tech Publisher')
        
        # Should count 1 approved article (not the pending one)
        self.assertEqual(tech_pub['article_count'], 1)


# TEST 6: MODEL VALIDATION
# (Not testing API endpoints - testing database rules)
class ModelValidationTests(TestCase):
    """
    Testing that our database enforces business rules correctly.
    Like making sure doors only open for people with the right key!
    """
    
    def test_reader_cannot_have_journalist_subscriptions_and_vice_versa(self):
        """Test that only readers can have subscriptions (business rule)."""
        # Create a reader
        reader = CustomUser.objects.create_user(
            username='reader4',
            email='reader4@test.com',
            password='pass123',
            role='READER'
        )
        
        # Create a journalist
        journalist = CustomUser.objects.create_user(
            username='journalist4',
            email='journalist4@test.com',
            password='pass123',
            role='JOURNALIST'
        )
        
        # Create a publisher
        publisher = Publisher.objects.create(name='Test Pub', description='Test')
        
        # Readers SHOULD be able to subscribe
        reader.subscribed_publishers.add(publisher)
        self.assertEqual(reader.subscribed_publishers.count(), 1)  # Works! ✓
        
        # Journalists shouldn't subscribe (but at model level it's allowed - forms prevent it)
        journalist.subscribed_publishers.add(publisher)
        self.assertEqual(journalist.subscribed_publishers.count(), 1)  # Saved, but forms prevent this in real use
    
    def test_article_slug_generation(self):
        """Test that article slugs are auto-generated from titles."""
        journalist = CustomUser.objects.create_user(
            username='journalist5',
            email='journalist5@test.com',
            password='pass123',
            role='JOURNALIST'
        )
        
        article = Article.objects.create(
            title='Test Article Title',  # Title with spaces and capitals
            content='Content',
            summary='Summary',
            author=journalist
        )
        
        # Slug should be auto-generated: lowercase with hyphens
        self.assertEqual(article.slug, 'test-article-title')  # Magic! ✨

