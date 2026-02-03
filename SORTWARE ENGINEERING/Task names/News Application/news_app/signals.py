from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Article, CustomUser
import requests


@receiver(pre_save, sender=Article)
def store_previous_approval_status(sender, instance, **kwargs):
    '''
    Store the previous approval status before saving.
    This allows us to detect when approval status changes from False to True.
    '''
    if instance.pk:
        try:
            instance._previous_is_approved = Article.objects.get(pk=instance.pk).is_approved
        except Article.DoesNotExist:
            instance._previous_is_approved = False
    else:
        instance._previous_is_approved = False


@receiver(post_save, sender=Article)
def handle_article_approval(sender, instance, created, **kwargs):
    '''
    Handle article approval by sending emails and posting to X.
    Triggered when an article's approval status changes from False to True.
    '''
    # Get previous approval status
    previous_approval = getattr(instance, '_previous_is_approved', False)
    
    # Check if article was just approved
    if instance.is_approved and not previous_approval:
        send_email_to_subscribers(instance)
        post_to_x(instance)


def get_subscribers_for_article(article):
    '''
    Collect all subscribers who should be notified about this article.
    Includes subscribers to the publisher and subscribers to the journalist.
    Returns a list of unique CustomUser objects.
    '''
    subscribers = set()
    
    # Get subscribers to the publisher
    if article.publisher:
        publisher_subscribers = article.publisher.subscribers.all()
        subscribers.update(publisher_subscribers)
    
    # Get subscribers to the journalist
    journalist_subscribers = article.author.journalist_subscribers.all()
    subscribers.update(journalist_subscribers)
    
    return list(subscribers)


def send_email_to_subscribers(article):
    '''
    Send email notification to all subscribers when article is approved.
    Subscribers include those subscribed to the publisher or the journalist.
    '''
    subscribers = get_subscribers_for_article(article)
    
    if not subscribers:
        print(f"No subscribers to notify for article: {article.title}")
        return
    
    # Build article URL
    article_url = f"http://127.0.0.1:8000/article/{article.slug}/"
    
    # Determine source information for email
    if article.publisher:
        source_info = f"from {article.publisher.name}"
    else:
        source_info = "as an independent article"
    
    # Send email to each subscriber
    for subscriber in subscribers:
        subject = f"New Article Published: {article.title}"
        
        message = f"""
Hello {subscriber.first_name or subscriber.username},

A new article has been published by {article.author.get_full_name() or article.author.username} {source_info}.

Title: {article.title}
Summary: {article.summary}

Read the full article here: {article_url}

---
You received this email because you are subscribed to {article.publisher.name if article.publisher else article.author.username}.
To manage your subscriptions, log in to your account.
"""
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email],
                fail_silently=False,
            )
            print(f"Email sent to {subscriber.email} for article: {article.title}")
        except Exception as e:
            print(f"Failed to send email to {subscriber.email}: {str(e)}")


def post_to_x(article):
    '''
    Post article announcement to X (Twitter) when approved.
    Uses X API v2 to create a tweet with article details.
    Fails gracefully if X API is not configured or request fails.
    '''
    # X API configuration
    X_API_URL = "https://api.twitter.com/2/tweets"
    X_BEARER_TOKEN = getattr(settings, 'X_BEARER_TOKEN', None)
    
    if not X_BEARER_TOKEN:
        print("X API token not configured. Skipping X post.")
        return
    
    # Build article URL
    article_url = f"http://127.0.0.1:8000/article/{article.slug}/"
    
    # Build tweet text
    tweet_text = f"""📰 New Article Published!

{article.title}

{article.summary[:100]}...

Read more: {article_url}

#{article.publisher.name.replace(' ', '') if article.publisher else 'IndependentJournalism'} #News
"""
    
    # Prepare API request
    headers = {
        "Authorization": f"Bearer {X_BEARER_TOKEN}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "text": tweet_text
    }
    
    # Send request to X API
    try:
        response = requests.post(X_API_URL, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 201:
            print(f"Successfully posted article to X: {article.title}")
        else:
            print(f"Failed to post to X. Status: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error posting to X: {str(e)}")
