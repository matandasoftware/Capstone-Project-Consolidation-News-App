
"""
models.py for Sticky Notes app

Defines the StickyNote model for storing note data.

Author: [Your Name]
"""

from django.db import models

class StickyNote(models.Model):
    """
    Model representing a sticky note with title, content, and timestamps.
    """


    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

