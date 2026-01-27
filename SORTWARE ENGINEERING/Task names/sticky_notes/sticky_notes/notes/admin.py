from django.contrib import admin
from .models import Note

# Register your models here.

class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    search_fields = ['title', 'content']
    list_filter = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    # Remove the "ADD NOTE +" button from the changelist page
    def changelist_view(self, request, extra_context=None):
        # Override to remove add button from this view
        extra_context = extra_context or {}
        extra_context['has_add_permission'] = False
        return super().changelist_view(request, extra_context)

admin.site.register(Note, NoteAdmin)