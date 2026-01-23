from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterForm(UserCreationForm):
    """User registration form with email and account type."""
    email = forms.EmailField(required=True)
    ACCOUNT_TYPES = [
        ('Vendors', 'Vendor - Sell Products'),
        ('Buyers', 'Buyer - Purchase Products'),
    ]
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPES, required=True, label="Account Type")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'account_type']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class LoginForm(AuthenticationForm):
    """User login form."""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class ForgotPasswordForm(forms.Form):
    """Forgot password form."""
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))


class PasswordResetForm(forms.Form):
    """Password reset form."""
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    password_conf = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
