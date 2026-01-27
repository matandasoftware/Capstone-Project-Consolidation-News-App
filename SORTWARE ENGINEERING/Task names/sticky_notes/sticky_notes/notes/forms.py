from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    """
    Note instance creation and updating form.
    
    Based on the Note model, this ModelForm automatically creates form fields.
    Note data is validated, cleaned, and saved by it.
    
    Fields:
        title: CharField for the title of the note
        content: TextField for the content of the note

    Meta class:
        It's a unique Django configuration class
        Since Django manages the created_at and updated_at fields
        automatically, they are not included.
    """
    
    class Meta:
        model = Note
        fields = ['title', 'content']
        