from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from .models import CustomUser, Publisher, Article, Newsletter


# Unregister Django's default Group admin
admin.site.unregister(Group)


@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    '''
    Custom admin for Groups to remove duplicate ADD button.
    '''
    def changelist_view(self, request, extra_context=None):
        '''Remove the duplicate ADD GROUP + button from the changelist page'''
        extra_context = extra_context or {}
        extra_context['has_add_permission'] = False
        return super().changelist_view(request, extra_context)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    '''
    Admin interface for CustomUser model.
    Extends Django's UserAdmin to include role and subscription fields.
    '''
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Subscriptions', {
            'fields': ('role', 'subscribed_publishers', 'subscribed_journalists'),
        }),
    )
    
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active', 'date_joined']
    list_filter = UserAdmin.list_filter + ('role',)
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    def changelist_view(self, request, extra_context=None):
        '''Remove the duplicate ADD USER + button from the changelist page'''
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

