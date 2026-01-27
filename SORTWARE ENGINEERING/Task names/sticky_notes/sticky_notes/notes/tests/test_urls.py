from django.test import SimpleTestCase
from django.urls import reverse, resolve
from notes import views


class NoteURLsTest(SimpleTestCase):
    """Test cases for URL routing"""
    
    def test_note_list_url_resolves(self):
        """Test that note_list URL resolves to correct view"""
        url = reverse('note_list')
        self.assertEqual(resolve(url).func, views.note_list)
    
    def test_note_detail_url_resolves(self):
        """Test that note_detail URL resolves to correct view"""
        url = reverse('note_detail', args=[1])
        self.assertEqual(resolve(url).func, views.note_detail)
    
    def test_note_create_url_resolves(self):
        """Test that note_create URL resolves to correct view"""
        url = reverse('note_create')
        self.assertEqual(resolve(url).func, views.note_create)
    
    def test_note_update_url_resolves(self):
        """Test that note_update URL resolves to correct view"""
        url = reverse('note_update', args=[1])
        self.assertEqual(resolve(url).func, views.note_update)
    
    def test_note_delete_url_resolves(self):
        """Test that note_delete URL resolves to correct view"""
        url = reverse('note_delete', args=[1])
        self.assertEqual(resolve(url).func, views.note_delete)
    
    def test_note_list_url_path(self):
        """Test that note_list has correct URL path"""
        url = reverse('note_list')
        self.assertEqual(url, '/notes/')
    
    def test_note_detail_url_path(self):
        """Test that note_detail has correct URL path"""
        url = reverse('note_detail', args=[5])
        self.assertEqual(url, '/notes/note/5/')
    
    def test_note_create_url_path(self):
        """Test that note_create has correct URL path"""
        url = reverse('note_create')
        self.assertEqual(url, '/notes/note/new/')
    
    def test_note_update_url_path(self):
        """Test that note_update has correct URL path"""
        url = reverse('note_update', args=[5])
        self.assertEqual(url, '/notes/note/5/edit/')
    
    def test_note_delete_url_path(self):
        """Test that note_delete has correct URL path"""
        url = reverse('note_delete', args=[5])
        self.assertEqual(url, '/notes/note/5/delete/')
