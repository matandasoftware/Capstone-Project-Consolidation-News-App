from django.test import TestCase
from notes.forms import NoteForm
from notes.models import Note


class NoteFormTest(TestCase):
    """Test cases for the NoteForm"""
    
    def test_note_form_valid_data(self):
        """Test that form is valid with correct data"""
        form_data = {
            'title': 'Test Title',
            'content': 'Test content'
        }
        form = NoteForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_note_form_missing_title(self):
        """Test that form is invalid without title"""
        form_data = {
            'content': 'Test content'
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_note_form_missing_content(self):
        """Test that form is invalid without content"""
        form_data = {
            'title': 'Test Title'
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
    
    def test_note_form_empty_data(self):
        """Test that form is invalid with empty data"""
        form = NoteForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
    
    def test_note_form_saves_correctly(self):
        """Test that form saves data correctly to database"""
        form_data = {
            'title': 'Test Title',
            'content': 'Test content'
        }
        form = NoteForm(data=form_data)
        self.assertTrue(form.is_valid())
        note = form.save(commit=False)
        note.author = 'Test Author'
        note.save()
        
        saved_note = Note.objects.get(title='Test Title')
        self.assertEqual(saved_note.content, 'Test content')
        self.assertEqual(saved_note.author, 'Test Author')
    
    def test_note_form_fields(self):
        """Test that form has only the expected fields"""
        form = NoteForm()
        self.assertEqual(list(form.fields.keys()), ['title', 'content'])
    
    def test_note_form_title_max_length(self):
        """Test that form validates title max length"""
        long_title = 'A' * 300  # Exceeds 255 character limit
        form_data = {
            'title': long_title,
            'content': 'Test content'
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
