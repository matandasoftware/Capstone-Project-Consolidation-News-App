from django.test import TestCase, Client
from django.urls import reverse
from notes.models import Note


class NoteViewsTest(TestCase):
    """Test cases for note views"""
    
    def setUp(self):
        """Set up test data and client before each test"""
        self.client = Client()
        self.note1 = Note.objects.create(
            title="First Note",
            content="First content",
            author="Author 1"
        )
        self.note2 = Note.objects.create(
            title="Second Note",
            content="Second content",
            author="Author 2"
        )
    
    def test_note_list_view_status_code(self):
        """Test that note list view returns 200 status"""
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_note_list_view_template(self):
        """Test that note list view uses correct template"""
        response = self.client.get(reverse('note_list'))
        self.assertTemplateUsed(response, 'notes/note_list.html')
    
    def test_note_list_view_displays_all_notes(self):
        """Test that all notes are displayed in the list"""
        response = self.client.get(reverse('note_list'))
        self.assertContains(response, "First Note")
        self.assertContains(response, "Second Note")
    
    def test_note_detail_view_status_code(self):
        """Test that note detail view returns 200 status"""
        response = self.client.get(reverse('note_detail', args=[self.note1.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_note_detail_view_template(self):
        """Test that note detail view uses correct template"""
        response = self.client.get(reverse('note_detail', args=[self.note1.pk]))
        self.assertTemplateUsed(response, 'notes/note_detail.html')
    
    def test_note_detail_view_displays_correct_note(self):
        """Test that detail view shows the correct note"""
        response = self.client.get(reverse('note_detail', args=[self.note1.pk]))
        self.assertContains(response, "First Note")
        self.assertContains(response, "First content")
    
    def test_note_detail_view_404_for_invalid_pk(self):
        """Test that detail view returns 404 for non-existent note"""
        response = self.client.get(reverse('note_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)
    
    def test_note_create_view_get(self):
        """Test that create view displays form on GET request"""
        response = self.client.get(reverse('note_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_form.html')
    
    def test_note_create_view_post_valid_data(self):
        """Test that valid POST data creates a new note"""
        data = {
            'title': 'New Note',
            'content': 'New content'
        }
        response = self.client.post(reverse('note_create'), data)
        self.assertEqual(Note.objects.count(), 3)
        self.assertTrue(Note.objects.filter(title='New Note').exists())
    
    def test_note_create_view_redirects_after_success(self):
        """Test that create view redirects to note list after success"""
        data = {
            'title': 'New Note',
            'content': 'New content'
        }
        response = self.client.post(reverse('note_create'), data)
        self.assertRedirects(response, reverse('note_list'))
    
    def test_note_update_view_get(self):
        """Test that update view displays form with existing data"""
        response = self.client.get(reverse('note_update', args=[self.note1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_form.html')
        self.assertContains(response, "First Note")
    
    def test_note_update_view_post_valid_data(self):
        """Test that valid POST data updates the note"""
        data = {
            'title': 'Updated Title',
            'content': 'Updated content'
        }
        response = self.client.post(reverse('note_update', args=[self.note1.pk]), data)
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.title, 'Updated Title')
        self.assertEqual(self.note1.content, 'Updated content')
    
    def test_note_update_view_redirects_after_success(self):
        """Test that update view redirects to detail after success"""
        data = {
            'title': 'Updated Title',
            'content': 'Updated content'
        }
        response = self.client.post(reverse('note_update', args=[self.note1.pk]), data)
        self.assertRedirects(response, reverse('note_detail', args=[self.note1.pk]))
    
    def test_note_delete_view_get(self):
        """Test that delete view displays confirmation page"""
        response = self.client.get(reverse('note_delete', args=[self.note1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_confirm_delete.html')
    
    def test_note_delete_view_post(self):
        """Test that POST request deletes the note"""
        response = self.client.post(reverse('note_delete', args=[self.note1.pk]))
        self.assertEqual(Note.objects.count(), 1)
        self.assertFalse(Note.objects.filter(pk=self.note1.pk).exists())
    
    def test_note_delete_view_redirects_after_success(self):
        """Test that delete view redirects to note list after deletion"""
        response = self.client.post(reverse('note_delete', args=[self.note1.pk]))
        self.assertRedirects(response, reverse('note_list'))
