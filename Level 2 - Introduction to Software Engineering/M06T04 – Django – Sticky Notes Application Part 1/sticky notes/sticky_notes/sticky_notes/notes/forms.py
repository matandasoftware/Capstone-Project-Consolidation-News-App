
"""
forms.py for Sticky Notes app

Defines forms for creating and updating sticky notes.

Author: [Your Name]
"""

from django import forms
from .models import StickyNote

class StickyNoteForm(forms.ModelForm):
    """
    Form for creating and updating StickyNote instances.
    Includes fields for title and content.
    """


    class Meta:
        model = StickyNote
        fields = ['title', 'content']

