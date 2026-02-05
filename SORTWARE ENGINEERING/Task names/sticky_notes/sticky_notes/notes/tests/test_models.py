from django.test import TestCase
from django.utils import timezone
from notes.models import Note
import time


class NoteModelTest(TestCase):
    """Test cases for the Note model"""
    
    def setUp(self):
        """Set up test data before each test method"""
        self.note = Note.objects.create(
            title="Test Note",
            content="This is test content",
            author="Test Author"
        )
    
    def test_note_creation(self):
        """Test that a note can be created successfully"""
        self.assertIsInstance(self.note, Note)
        self.assertEqual(self.note.title, "Test Note")
        self.assertEqual(self.note.content, "This is test content")
        self.assertEqual(self.note.author, "Test Author")
    
    def test_note_str_representation(self):
        """Test the string representation of a note"""
        self.assertEqual(str(self.note), "Test Note")
    
    def test_note_has_created_at_timestamp(self):
        """Test that created_at is automatically set"""
        self.assertIsNotNone(self.note.created_at)
        self.assertLessEqual(self.note.created_at, timezone.now())
    
    def test_note_has_updated_at_timestamp(self):
        """Test that updated_at is automatically set"""
        self.assertIsNotNone(self.note.updated_at)
        self.assertLessEqual(self.note.updated_at, timezone.now())
    
    def test_note_update_changes_updated_at(self):
        """Test that updating a note changes the updated_at timestamp"""
        original_updated_at = self.note.updated_at
        time.sleep(0.001)  # Small delay to ensure timestamp changes
        self.note.content = "Updated content"
        self.note.save()
        self.assertGreater(self.note.updated_at, original_updated_at)
    
    def test_note_title_max_length(self):
        """Test that title has correct max length"""
        max_length = self.note._meta.get_field('title').max_length
        self.assertEqual(max_length, 255)
    
    def test_note_author_max_length(self):
        """Test that author has correct max length"""
        max_length = self.note._meta.get_field('author').max_length
        self.assertEqual(max_length, 100)
