from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django import forms
from django.db import connection
from .models import CustomUser, Publisher, Article, Newsletter


# Unregister Django's default Group admin
admin.site.unregister(Group)


@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_add_permission'] = False
        return super().changelist_view(request, extra_context)


# Custom form that explicitly defines the role field
class CustomUserAdminForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'role-select'})
    )
    
    class Meta:
        model = CustomUser
        fields = '__all__'


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    COMPLETELY REWRITTEN - Simple and direct approach with explicit form
    """
    form = CustomUserAdminForm  # Use our custom form
    list_display = ['username', 'email', 'role', 'get_groups', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email']
    filter_horizontal = ['subscribed_publishers', 'subscribed_journalists', 'groups']
    
    # Simple field list - no fieldsets complexity
    fields = [
        'username', 'password', 'email', 'first_name', 'last_name',
        'role', 'is_staff', 'is_active', 'is_superuser',
        'groups', 'subscribed_publishers', 'subscribed_journalists'
    ]
    
    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = 'Groups'
    
    def save_model(self, request, obj, form, change):
        """
        Override save_model to ensure role changes are properly saved.
        """
        # Get the role the user selected in the form
        selected_role = request.POST.get('role', 'READER')
        
        # FORCE the role before any save
        obj.role = selected_role
        
        # Save the object
        super().save_model(request, obj, form, change)
        
        # Check if it stuck
        obj.refresh_from_db()
        
        # If Django reset it, use raw SQL
        if obj.role != selected_role:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE news_app_customuser SET role = %s WHERE id = %s",
                    [selected_role, obj.id]
                )
            obj.refresh_from_db()
        
        # Now assign groups
        obj._assign_to_group()
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['has_add_permission'] = False
        return super().changelist_view(request, extra_context)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    '''
    Admin interface for Publisher model.
    Shows publisher details and staff counts.
    '''
    list_display = ['name', 'website', 'created_at', 'get_editors_count', 'get_journalists_count']
    search_fields = ['name', 'description']
    filter_horizontal = ['editors', 'journalists']
    
    def changelist_view(self, request, extra_context=None):
        '''Remove the duplicate ADD PUBLISHER + button from the changelist page'''
        extra_context = extra_context or {}
        extra_context['has_add_permission'] = False
        return super().changelist_view(request, extra_context)
    
    def get_editors_count(self, obj):
        '''Return count of editors for this publisher'''
        return obj.editors.count()
    get_editors_count.short_description = 'Editors'
    
    def get_journalists_count(self, obj):
        '''Return count of journalists for this publisher'''
        return obj.journalists.count()
    get_journalists_count.short_description = 'Journalists'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    '''
    Admin interface for Article model.
    Shows article details, approval status, and filters.
    '''
    list_display = ['title', 'author', 'publisher', 'is_approved', 'is_independent', 'created_at']
    list_filter = ['is_approved', 'is_independent', 'created_at', 'author', 'publisher']
    search_fields = ['title', 'content', 'summary', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['approved_by', 'approved_at', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    def changelist_view(self, request, extra_context=None):
        '''Remove the duplicate ADD ARTICLE + button from the changelist page'''
        extra_context = extra_context or {}
        extra_context['has_add_permission'] = False
        return super().changelist_view(request, extra_context)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    '''
    Admin interface for Newsletter model.
    Shows newsletter details and filters.
    '''
    list_display = ['title', 'author', 'publisher', 'is_independent', 'created_at']
    list_filter = ['is_independent', 'created_at', 'author', 'publisher']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    def changelist_view(self, request, extra_context=None):
        '''Remove the duplicate ADD NEWSLETTER + button from the changelist page'''
        extra_context = extra_context or {}
        extra_context['has_add_permission'] = False
        return super().changelist_view(request, extra_context)

