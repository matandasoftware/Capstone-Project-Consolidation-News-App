"""
Django Signals for the News Application.

This module defines signal handlers for automated actions:
- Article approval notifications: Email editors when articles submitted
- User creation handlers: Set up initial permissions and groups
- Post-save actions: Trigger related updates

Uses Django's signal dispatcher for event-driven functionality.
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Article, CustomUser
from .twitter_utils import tweet_article
import logging

logger = logging.getLogger(__name__)


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
    """
    Handle article approval by sending emails and posting to X.
    Triggered when an article's approval status changes from False to True.
    """
    previous_approval = getattr(instance, '_previous_is_approved', False)
    
    if instance.is_approved and not previous_approval:
        send_email_to_subscribers(instance)
        tweet_article(instance)


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


@receiver(pre_save, sender=CustomUser)
def store_previous_role(sender, instance, **kwargs):
    '''
    Store the previous role before saving.
    This allows us to detect when a user's role changes.
    '''
    if instance.pk:
        try:
            instance._previous_role = CustomUser.objects.get(pk=instance.pk).role
        except CustomUser.DoesNotExist:
            instance._previous_role = None
    else:
        instance._previous_role = None


@receiver(post_save, sender=CustomUser)
def invalidate_user_sessions_on_role_change(sender, instance, created, **kwargs):
    '''
    When a user's role changes, invalidate all their active sessions.
    This forces them to log in again to get the updated role/permissions.
    '''
    if not created:
        previous_role = getattr(instance, '_previous_role', None)
        if previous_role and previous_role != instance.role:
            # Role changed - invalidate all sessions for this user
            from django.contrib.sessions.models import Session
            from django.contrib.auth import get_user_model
            from django.utils import timezone
            
            # Get all active sessions
            active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
            
            # Check each session to see if it belongs to this user
            for session in active_sessions:
                session_data = session.get_decoded()
                session_user_id = session_data.get('_auth_user_id')
                if session_user_id and int(session_user_id) == instance.pk:
                    # Delete this session to force re-login
                    session.delete()
                    logger.info(f"Invalidated session for user {instance.username} due to role change from {previous_role} to {instance.role}")



