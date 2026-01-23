from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin


# Unregister the original models
admin.site.unregister(User)
admin.site.unregister(Group)


# Re-register with custom admin (no duplicate button)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin without duplicate add button."""
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_add_permission'] = False
        return super().changelist_view(request, extra_context)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    """Custom Group admin without duplicate add button."""
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_add_permission'] = False
        return super().changelist_view(request, extra_context)
