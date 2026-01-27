from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import EmailMessage
from .forms import RegisterForm, LoginForm, ForgotPasswordForm, PasswordResetForm
from .models import ResetToken
import secrets
from datetime import datetime, timedelta
from hashlib import sha1


# Helper Functions

def verify_username(username):
    """Check if username is available."""
    return not User.objects.filter(username=username).exists()


def verify_password(password):
    """Check if password meets requirements."""
    return len(password) >= 8


def change_user_password(username, new_password):
    """Change user password."""
    user = User.objects.get(username=username)
    user.set_password(new_password)
    user.save()


def build_email(user, reset_url):
    """Build password reset email."""
    subject = "Password Reset"
    user_email = user.email
    domain_email = "noreply@ecommerce.com"
    body = f"Hi {user.username},\n\nReset your password:\n{reset_url}\n\nExpires in 5 minutes."
    email = EmailMessage(subject, body, domain_email, [user_email])
    return email


def generate_reset_url(user):
    """Generate password reset URL with token."""
    domain = "http://127.0.0.1:8000/"
    app_name = "accounts"
    url = f"{domain}{app_name}/reset_password/"
    token = str(secrets.token_urlsafe(16))
    expiry_date = datetime.now() + timedelta(minutes=5)
    reset_token = ResetToken.objects.create(
        user=user,
        token=sha1(token.encode()).hexdigest(),
        expiry_date=expiry_date
    )
    url += f"{token}/"
    return url


# Registration

def register_user(request):
    """User registration with vendor/buyer selection."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            account_type = form.cleaned_data['account_type']

            if verify_username(username) and verify_password(password):
                user = User.objects.create_user(username=username, password=password)
                user.email = email

                # Add user to group (Vendors or Buyers)
                # Capitalize and pluralize to match group names: Vendors, Buyers
                group_name = account_type.capitalize() + 's'
                user_group, created = Group.objects.get_or_create(name=group_name)
                user.groups.add(user_group)
                user.save()

                login(request, user)
                messages.success(request, f'Welcome {username}! Your {account_type} account has been created.')
                return redirect('accounts:welcome')
            else:
                messages.error(request, 'Username taken or password too weak.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


# Login & Logout

def login_user(request):
    """User login."""
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Set session expiry (10 minutes of inactivity)
                request.session.set_expiry(600)
                messages.success(request, f'Welcome back, {username}!')
                return HttpResponseRedirect(reverse('accounts:welcome'))
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_user(request):
    """User logout (preserves cart)."""
    if request.user.is_authenticated:
        # Save cart before logout
        cart = request.session.get('cart', {})
        
        logout(request)
        
        # Restore cart after logout (allows anonymous shopping)
        request.session['cart'] = cart
        request.session.modified = True
        
        messages.success(request, 'You have been logged out. Your cart has been preserved.')
    return HttpResponseRedirect(reverse('accounts:login'))


# Protected Views

@login_required(login_url='/accounts/login/')
def welcome(request):
    """Welcome page (protected)."""
    return render(request, 'accounts/welcome.html')


# Password Reset

def send_password_reset(request):
    """Send password reset email."""
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=user_email)
                url = generate_reset_url(user)
                email = build_email(user, url)
                email.send()
                messages.success(request, 'Password reset link sent to your email!')
                return HttpResponseRedirect(reverse('accounts:login'))
            except User.DoesNotExist:
                messages.error(request, 'No account found with that email.')
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'accounts/forgot_password.html', {'form': form})


def reset_user_password(request, token):
    """Validate token and show password reset form."""
    try:
        hashed_token = sha1(token.encode()).hexdigest()
        user_token = ResetToken.objects.get(token=hashed_token, used=False)
        
        # Check if token expired
        if user_token.expiry_date.replace(tzinfo=None) < datetime.now():
            user_token.delete()
            messages.error(request, 'This reset link has expired.')
            return redirect('accounts:forgot_password')
        
        # Store in session
        request.session['reset_user'] = user_token.user.username
        request.session['reset_token'] = token
        
        return render(request, 'accounts/password_reset.html', {'token': user_token, 'form': PasswordResetForm()})
    except ResetToken.DoesNotExist:
        messages.error(request, 'Invalid reset link.')
        return redirect('accounts:forgot_password')


def reset_password(request):
    """Complete password reset."""
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = request.session.get('reset_user')
            token = request.session.get('reset_token')
            password = form.cleaned_data['password']
            password_conf = form.cleaned_data['password_conf']

            if password == password_conf:
                # Get user and change password properly
                user = User.objects.get(username=username)
                user.set_password(password)
                user.save()
                # Mark token as used and delete
                hashed_token = sha1(token.encode()).hexdigest()
                ResetToken.objects.filter(token=hashed_token).update(used=True)
                # Clear session
                del request.session['reset_user']
                del request.session['reset_token']
                messages.success(request, 'Password reset successful! Please login.')
                return HttpResponseRedirect(reverse('accounts:login'))
            else:
                messages.error(request, 'Passwords do not match.')
                return redirect('accounts:password_reset_token', token=token)
    
    return HttpResponseRedirect(reverse('accounts:login'))