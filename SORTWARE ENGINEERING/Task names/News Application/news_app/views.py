"""
Views for the News Application.

This module contains all view functions that handle HTTP requests including:
- Public views: Homepage, article details
- Authentication: Login, logout, registration
- Reader views: Dashboard, browse publishers/journalists, subscriptions
- Journalist views: Create/edit articles and newsletters
- Editor views: Approve articles
- Publisher management: Create publishers on-the-fly

Each view includes permission checks and role-based access control.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils import timezone
from django.db import models
from django.http import JsonResponse
from .models import CustomUser, Publisher, Article, Newsletter
from .forms import UserRegistrationForm, ArticleForm, NewsletterForm, PublisherForm


# Public Views

def home(request):
    """Display homepage with approved articles."""
    articles = Article.objects.filter(is_approved=True).order_by('-created_at')[:10]
    return render(request, 'news_app/home.html', {'articles': articles})


def article_detail(request, slug):
    """Display single article by slug."""
    article = get_object_or_404(Article, slug=slug, is_approved=True)
    return render(request, 'news_app/article_detail.html', {'article': article})


# Authentication Views

def register(request):
    """User registration."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'news_app/register.html', {'form': form})


def login_view(request):
    """User login."""
    from django.contrib.auth.forms import AuthenticationForm
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect based on role
            if user.role == 'READER':
                return redirect('reader_dashboard')
            elif user.role == 'JOURNALIST':
                return redirect('journalist_dashboard')
            elif user.role == 'EDITOR':
                return redirect('editor_dashboard')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'news_app/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout."""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


# Reader Views

@login_required
def reader_dashboard(request):
    """Reader dashboard with subscribed content."""
    if request.user.role != 'READER':
        messages.error(request, 'Access denied. This page is for readers only.')
        return redirect('home')
    
    # Get subscribed content
    subscribed_publishers = request.user.subscribed_publishers.all()
    subscribed_journalists = request.user.subscribed_journalists.all()
    
    # Get articles from subscriptions
    articles = Article.objects.filter(
        is_approved=True
    ).filter(
        models.Q(publisher__in=subscribed_publishers) | 
        models.Q(author__in=subscribed_journalists)
    ).order_by('-created_at')
    
    context = {
        'subscribed_publishers': subscribed_publishers,
        'subscribed_journalists': subscribed_journalists,
        'articles': articles,
    }
    return render(request, 'news_app/reader_dashboard.html', context)


@login_required
def browse_publishers(request):
    """Browse all publishers."""
    if request.user.role != 'READER':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    publishers = Publisher.objects.all()
    return render(request, 'news_app/browse_publishers.html', {'publishers': publishers})


@login_required
def browse_journalists(request):
    """Browse all journalists."""
    if request.user.role != 'READER':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    journalists = CustomUser.objects.filter(role='JOURNALIST')
    return render(request, 'news_app/browse_journalists.html', {'journalists': journalists})


@login_required
def subscribe_publisher(request, pk):
    """Subscribe to a publisher."""
    if request.user.role != 'READER':
        messages.error(request, 'Only readers can subscribe.')
        return redirect('home')
    
    publisher = get_object_or_404(Publisher, pk=pk)
    request.user.subscribed_publishers.add(publisher)
    messages.success(request, f'Subscribed to {publisher.name}!')
    return redirect('browse_publishers')


@login_required
def unsubscribe_publisher(request, pk):
    """Unsubscribe from a publisher."""
    if request.user.role != 'READER':
        messages.error(request, 'Only readers can unsubscribe.')
        return redirect('home')
    
    publisher = get_object_or_404(Publisher, pk=pk)
    request.user.subscribed_publishers.remove(publisher)
    messages.success(request, f'Unsubscribed from {publisher.name}.')
    return redirect('reader_dashboard')


@login_required
def subscribe_journalist(request, pk):
    """Subscribe to a journalist."""
    if request.user.role != 'READER':
        messages.error(request, 'Only readers can subscribe.')
        return redirect('home')
    
    journalist = get_object_or_404(CustomUser, pk=pk, role='JOURNALIST')
    request.user.subscribed_journalists.add(journalist)
    messages.success(request, f'Subscribed to {journalist.username}!')
    return redirect('browse_journalists')


@login_required
def unsubscribe_journalist(request, pk):
    """Unsubscribe from a journalist."""
    if request.user.role != 'READER':
        messages.error(request, 'Only readers can unsubscribe.')
        return redirect('home')
    
    journalist = get_object_or_404(CustomUser, pk=pk, role='JOURNALIST')
    request.user.subscribed_journalists.remove(journalist)
    messages.success(request, f'Unsubscribed from {journalist.username}.')
    return redirect('reader_dashboard')


# Journalist Views

@login_required
def journalist_dashboard(request):
    """Journalist dashboard with their articles."""
    if request.user.role != 'JOURNALIST':
        messages.error(request, 'Access denied. This page is for journalists only.')
        return redirect('home')
    
    articles = Article.objects.filter(author=request.user).order_by('-created_at')
    newsletters = Newsletter.objects.filter(author=request.user).order_by('-created_at')
    
    context = {
        'articles': articles,
        'newsletters': newsletters,
    }
    return render(request, 'news_app/journalist_dashboard.html', context)


@login_required
def article_create(request):
    """Create new article."""
    if request.user.role != 'JOURNALIST':
        messages.error(request, 'Only journalists can create articles.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Article created! Waiting for approval.')
            return redirect('journalist_dashboard')
    else:
        form = ArticleForm()
    return render(request, 'news_app/article_form.html', {'form': form})


@login_required
def article_update(request, pk):
    """Update existing article."""
    article = get_object_or_404(Article, pk=pk)
    
    # Check permission
    if request.user.role != 'JOURNALIST' or article.author != request.user:
        messages.error(request, 'You can only edit your own articles.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated successfully!')
            return redirect('journalist_dashboard')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'news_app/article_form.html', {'form': form, 'article': article})


@login_required
def article_delete(request, pk):
    """Delete article."""
    article = get_object_or_404(Article, pk=pk)
    
    # Check permission
    if request.user.role != 'JOURNALIST' or article.author != request.user:
        messages.error(request, 'You can only delete your own articles.')
        return redirect('home')
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article deleted.')
        return redirect('journalist_dashboard')
    return render(request, 'news_app/article_confirm_delete.html', {'article': article})


@login_required
def newsletter_create(request):
    """Create new newsletter."""
    if request.user.role != 'JOURNALIST':
        messages.error(request, 'Only journalists can create newsletters.')
        return redirect('home')
    
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            messages.success(request, 'Newsletter created!')
            return redirect('journalist_dashboard')
    else:
        form = NewsletterForm()
    return render(request, 'news_app/newsletter_form.html', {'form': form})


@login_required
def newsletter_update(request, pk):
    """Update existing newsletter."""
    newsletter = get_object_or_404(Newsletter, pk=pk)
    
    # Check permission
    if request.user.role != 'JOURNALIST' or newsletter.author != request.user:
        messages.error(request, 'You can only edit your own newsletters.')
        return redirect('home')
    
    if request.method == 'POST':
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Newsletter updated successfully!')
            return redirect('journalist_dashboard')
    else:
        form = NewsletterForm(instance=newsletter)
    return render(request, 'news_app/newsletter_form.html', {'form': form, 'newsletter': newsletter})


@login_required
def newsletter_delete(request, pk):
    """Delete newsletter."""
    newsletter = get_object_or_404(Newsletter, pk=pk)
    
    # Check permission
    if request.user.role != 'JOURNALIST' or newsletter.author != request.user:
        messages.error(request, 'You can only delete your own newsletters.')
        return redirect('home')
    
    if request.method == 'POST':
        newsletter.delete()
        messages.success(request, 'Newsletter deleted.')
        return redirect('journalist_dashboard')
    return render(request, 'news_app/newsletter_confirm_delete.html', {'newsletter': newsletter})


# Editor Views

@login_required
def editor_dashboard(request):
    """Editor dashboard with pending articles."""
    if request.user.role != 'EDITOR':
        messages.error(request, 'Access denied. This page is for editors only.')
        return redirect('home')
    
    pending_articles = Article.objects.filter(is_approved=False).order_by('-created_at')
    approved_articles = Article.objects.filter(is_approved=True).order_by('-approved_at')[:10]
    
    context = {
        'pending_articles': pending_articles,
        'approved_articles': approved_articles,
    }
    return render(request, 'news_app/editor_dashboard.html', context)


@login_required
@permission_required('news_app.approve_article', raise_exception=True)
def article_approve(request, pk):
    """Approve article."""
    if request.user.role != 'EDITOR':
        messages.error(request, 'Only editors can approve articles.')
        return redirect('home')
    
    article = get_object_or_404(Article, pk=pk)
    
    if request.method == 'POST':
        article.is_approved = True
        article.approved_by = request.user
        article.approved_at = timezone.now()
        article.published_at = timezone.now()
        article.save()
        
        messages.success(request, f'Article "{article.title}" has been approved and published!')
        return redirect('editor_dashboard')
    
    return render(request, 'news_app/article_approve.html', {'article': article})


@login_required
@permission_required('news_app.add_publisher', raise_exception=True)
def publisher_create(request):
    """Create a new publisher. Supports both form submission and AJAX JSON requests."""
    # Handle AJAX JSON request
    if request.headers.get('Content-Type') == 'application/json':
        import json
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            description = data.get('description', '').strip()
            website = data.get('website', '').strip()
            
            # Validation
            if not name:
                return JsonResponse({'success': False, 'message': 'Publisher name is required.'})
            
            # Check if publisher already exists
            if Publisher.objects.filter(name__iexact=name).exists():
                return JsonResponse({'success': False, 'message': f'Publisher "{name}" already exists.'})
            
            # Create publisher
            publisher = Publisher.objects.create(
                name=name,
                description=description,
                website=website
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Publisher "{publisher.name}" created successfully!',
                'publisher': {
                    'id': publisher.id,
                    'name': publisher.name,
                    'description': publisher.description,
                    'website': publisher.website
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    # Handle regular form submission (for backward compatibility)
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save()
            messages.success(request, f'Publisher "{publisher.name}" created successfully!')
            
            # If opened in a new tab from article/newsletter form, close window
            if request.GET.get('next'):
                return render(request, 'news_app/publisher_created.html', {'publisher': publisher})
            
            # Otherwise redirect to home
            return redirect('home')
    else:
        form = PublisherForm()
    
    return render(request, 'news_app/publisher_form.html', {'form': form})


