from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from notes.models import Note


class NoteAdminTest(TestCase):
    """Test cases for Note admin functionality"""
    
    def setUp(self):
        """Set up admin user and test data"""
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        self.client.login(username='admin', password='admin123')
        
        self.note = Note.objects.create(
            title="Admin Test Note",
            content="Admin test content",
            author="Admin Author"
        )
    
    def test_admin_note_list_accessible(self):
        """Test that admin note list page is accessible"""
        response = self.client.get('/admin/notes/note/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_note_changelist_columns(self):
        """Test that changelist displays correct columns"""
        response = self.client.get('/admin/notes/note/')
        self.assertContains(response, 'Admin Test Note')
    
    def test_admin_note_add_button_hidden_in_changelist(self):
        """Test that ADD NOTE button is hidden in changelist"""
        response = self.client.get('/admin/notes/note/')
        # Check that the context variable has_add_permission is False
        self.assertFalse(response.context['has_add_permission'])
    
    def test_admin_note_search_functionality(self):
        """Test that search works in admin"""
        response = self.client.get('/admin/notes/note/?q=Admin')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Test Note')
    
    def test_admin_note_filter_by_created_date(self):
        """Test that filtering by created date is available"""
        response = self.client.get('/admin/notes/note/')
        self.assertContains(response, 'created at')
    
    def test_admin_note_detail_accessible(self):
        """Test that individual note is accessible in admin"""
        response = self.client.get(f'/admin/notes/note/{self.note.pk}/change/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Test Note')
    
    def test_admin_note_delete_accessible(self):
        """Test that delete confirmation page is accessible"""
        response = self.client.get(f'/admin/notes/note/{self.note.pk}/delete/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_note_ordering(self):
        """Test that notes are ordered by creation date descending"""
        note2 = Note.objects.create(
            title="Second Note",
            content="Second content",
            author="Second Author"
        )
        response = self.client.get('/admin/notes/note/')
        # The newer note should appear before the older one
        content = response.content.decode()
        pos_second = content.find('Second Note')
        pos_first = content.find('Admin Test Note')
        self.assertLess(pos_second, pos_first)
