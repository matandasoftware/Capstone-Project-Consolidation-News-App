# Register your models here.
from django.contrib import admin
from .models import StickyNote

@admin.register(StickyNote)
class StickyNoteAdmin(admin.ModelAdmin):
    """
    Admin interface options for StickyNote model.
    """
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')