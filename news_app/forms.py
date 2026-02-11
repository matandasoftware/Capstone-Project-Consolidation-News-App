"""
Forms for the News Application.

This module defines Django forms for user input and validation:
- CustomUserCreationForm: User registration with role selection
- CustomUserChangeForm: User profile updates
- ArticleForm: Create and edit news articles
- NewsletterForm: Create and edit newsletters
- PublisherForm: Create new publishers

Forms include field validation and custom widgets for better UX.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Article, Newsletter, Publisher


class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration with role selection.
    Prevents self-registration as editor.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2']
    
    def clean_role(self):
        """Prevent users from self-registering as editors."""
        role = self.cleaned_data.get('role')
        if role == 'EDITOR':
            raise forms.ValidationError('Editor accounts must be created by administrators.')
        return role


class ArticleForm(forms.ModelForm):
    """Form for creating and editing articles."""
    class Meta:
        model = Article
        fields = ['title', 'content', 'summary', 'publisher']


class NewsletterForm(forms.ModelForm):
    """Form for creating and editing newsletters."""
    class Meta:
        model = Newsletter
        fields = ['title', 'content', 'publisher']


class PublisherForm(forms.ModelForm):
    """Form for creating publishers on the spot."""
    class Meta:
        model = Publisher
        fields = ['name', 'description', 'website']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }





