# EXPLANATION: news_app/signals.py

## What This File Is
The signals.py file contains Django signal handlers that automatically perform actions when certain events occur. Specifically, it handles what happens when an article is approved by an editor.

## Why This File Is Important
Signals allow us to decouple logic and automatically trigger actions without modifying the main approval view. When an article is approved, we need to:
1. Send email notifications to all subscribers
2. Post the article to X (Twitter)

This file implements those automated actions using Django's signal system.

## Detailed Code Breakdown

### Import Section
```python
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Article, CustomUser
import requests
```

**What each import does:**
- `post_save` - Signal sent after a model is saved to database
- `pre_save` - Signal sent before a model is saved (we use this to detect changes)
- `receiver` - Decorator to connect functions to signals
- `send_mail` - Django function to send emails
- `settings` - Access to Django settings (EMAIL configuration)
- `Article, CustomUser` - Our models
- `requests` - Python library for making HTTP requests (for X API)

---

## Detecting Article Approval

### Problem
We need to know when `is_approved` changes from False to True. We can't tell this in `post_save` alone because the old value is already overwritten.

### Solution: Store Old Value in pre_save
```python
@receiver(pre_save, sender=Article)
def store_previous_approval_status(sender, instance, **kwargs):
```
**What this does:**
- `@receiver(pre_save, sender=Article)` - This function runs BEFORE Article is saved
- `sender` - The model class (Article)
- `instance` - The specific article being saved
- `**kwargs` - Additional arguments Django passes

```python
if instance.pk:
    try:
        instance._previous_is_approved = Article.objects.get(pk=instance.pk).is_approved
    except Article.DoesNotExist:
        instance._previous_is_approved = False
else:
    instance._previous_is_approved = False
```

**What this does:**
- `if instance.pk` - Check if article already exists (has primary key)
- `Article.objects.get(pk=instance.pk)` - Get current version from database
- `.is_approved` - Get the old approval status
- `instance._previous_is_approved` - Store old value as temporary attribute
- If article doesn't exist yet, set to False (new articles start as not approved)

**Why this matters:** We can now compare old and new values in post_save to detect when approval happens.

---

## Handling Article Approval

### Function Definition
```python
@receiver(post_save, sender=Article)
def handle_article_approval(sender, instance, created, **kwargs):
```
**What this does:**
- `@receiver(post_save, sender=Article)` - Runs AFTER Article is saved
- `created` - Boolean: True if this is a new article, False if update
- All other parameters same as before

### Check if Article Was Just Approved
```python
previous_approval = getattr(instance, '_previous_is_approved', False)
```
**What this does:**
- `getattr(instance, '_previous_is_approved', False)` - Get the old approval status we stored
- If attribute doesn't exist (shouldn't happen), default to False

```python
if instance.is_approved and not previous_approval:
```
**What this does:**
- `instance.is_approved` - New status is approved (True)
- `not previous_approval` - Old status was not approved (False)
- Combined: Article was just approved (status changed from False to True)

### Perform Approval Actions
```python
    send_email_to_subscribers(instance)
    post_to_x(instance)
```
**What this does:**
- Call helper functions to send emails and post to X
- Only happens when article is first approved

---

## Collecting Subscribers

### Function Definition
```python
def get_subscribers_for_article(article):
```
**Purpose:** Find all readers who should receive notification about this article.

### Collect Publisher Subscribers
```python
subscribers = set()

if article.publisher:
    publisher_subscribers = article.publisher.subscribers.all()
    subscribers.update(publisher_subscribers)
```
**What this does:**
- `subscribers = set()` - Create empty set (sets automatically remove duplicates)
- `if article.publisher` - Check if article has a publisher
- `article.publisher.subscribers.all()` - Get all readers subscribed to this publisher
- `subscribers.update(publisher_subscribers)` - Add them to our set

**Why set?** A reader might be subscribed to both publisher AND journalist. Set prevents sending duplicate emails.

### Collect Journalist Subscribers
```python
journalist_subscribers = article.author.journalist_subscribers.all()
subscribers.update(journalist_subscribers)
```
**What this does:**
- `article.author.journalist_subscribers.all()` - Get all readers subscribed to the article's author
- Add them to the set (duplicates automatically removed)

### Return Result
```python
return list(subscribers)
```
**What this does:**
- Convert set back to list
- Returns list of unique CustomUser objects who should be notified

---

## Sending Email Notifications

### Function Definition
```python
def send_email_to_subscribers(article):
```
**Purpose:** Send email to all subscribers about newly approved article.

### Get Subscribers
```python
subscribers = get_subscribers_for_article(article)

if not subscribers:
    print(f"No subscribers to notify for article: {article.title}")
    return
```
**What this does:**
- Get list of subscribers using helper function
- If no subscribers, print message and exit early
- `return` - Stop function execution if no one to notify

### Build Article URL
```python
article_url = f"http://127.0.0.1:8000/article/{article.slug}/"
```
**What this does:**
- Create full URL to article
- Uses article's slug for SEO-friendly URL
- `f"..."` - F-string for string interpolation

**Note:** In production, replace `127.0.0.1:8000` with actual domain.

### Determine Source Information
```python
if article.publisher:
    source_info = f"from {article.publisher.name}"
else:
    source_info = "as an independent article"
```
**What this does:**
- If article has publisher, include publisher name in email
- If independent, indicate it's independent
- Makes email more informative

### Send Email to Each Subscriber
```python
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
```

**What this does:**
- `for subscriber in subscribers` - Loop through each subscriber
- `subject` - Email subject line with article title
- `message` - Multi-line email body using triple quotes
- `{subscriber.first_name or subscriber.username}` - Use first name if available, else username
- `{article.author.get_full_name() or article.author.username}` - Author's full name or username
- Includes article title, summary, and link
- Tells reader why they received email (publisher or journalist subscription)

### Send the Email
```python
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
```

**What this does:**
- `try...except` - Error handling (defensive coding)
- `send_mail()` - Django function to send email
  * `subject` - Email subject
  * `message` - Email body
  * `from_email` - Sender address (from settings)
  * `recipient_list` - List of recipient emails (just one in this case)
  * `fail_silently=False` - Raise exceptions if email fails
- Print success message
- If error occurs, catch it and print error message
- Even if one email fails, others still get sent

---

## Posting to X (Twitter)

### Function Definition
```python
def post_to_x(article):
```
**Purpose:** Automatically post article to X (Twitter) when approved.

### Configuration
```python
X_API_URL = "https://api.twitter.com/2/tweets"
X_BEARER_TOKEN = getattr(settings, 'X_BEARER_TOKEN', None)
```
**What this does:**
- `X_API_URL` - X API endpoint for creating tweets
- `getattr(settings, 'X_BEARER_TOKEN', None)` - Get token from settings, or None if not configured
- Token should be added to settings.py for production use

### Check if Configured
```python
if not X_BEARER_TOKEN:
    print("X API token not configured. Skipping X post.")
    return
```
**What this does:**
- Check if token is set
- If not, print message and exit
- Prevents errors when X API isn't configured (development mode)

### Build Tweet Content
```python
article_url = f"http://127.0.0.1:8000/article/{article.slug}/"

tweet_text = f"""📰 New Article Published!

{article.title}

{article.summary[:100]}...

Read more: {article_url}

#{article.publisher.name.replace(' ', '') if article.publisher else 'IndependentJournalism'} #News
"""
```

**What this does:**
- Create article URL
- Build tweet text:
  * Emoji for attention (📰)
  * Article title
  * First 100 characters of summary with ellipsis
  * Link to full article
  * Hashtags: publisher name (spaces removed) or "IndependentJournalism"
  * Generic #News hashtag

### Prepare API Request
```python
headers = {
    "Authorization": f"Bearer {X_BEARER_TOKEN}",
    "Content-Type": "application/json",
}

payload = {
    "text": tweet_text
}
```
**What this does:**
- `headers` - HTTP headers for authentication
  * `Authorization` - Bearer token authentication
  * `Content-Type` - Sending JSON data
- `payload` - Request body with tweet text

### Send Request to X API
```python
try:
    response = requests.post(X_API_URL, json=payload, headers=headers, timeout=10)
    
    if response.status_code == 201:
        print(f"Successfully posted article to X: {article.title}")
    else:
        print(f"Failed to post to X. Status: {response.status_code}, Response: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"Error posting to X: {str(e)}")
```

**What this does:**
- `try...except` - Error handling (defensive coding)
- `requests.post()` - Send POST request to X API
  * `X_API_URL` - Endpoint
  * `json=payload` - Send data as JSON
  * `headers=headers` - Include auth headers
  * `timeout=10` - Wait max 10 seconds for response
- Check `response.status_code`:
  * `201` - Success (tweet created)
  * Other - Error occurred
- Print appropriate message
- Catch `RequestException` for network errors
- Even if X post fails, email still sends (failure doesn't break article approval)

**Why fail gracefully?** Article approval shouldn't fail just because X API is down. Log the error and continue.

---

## Signal Registration (apps.py)

### Not in this file, but important
This file needs to be imported in `apps.py` for signals to work:

```python
# In news_app/apps.py
class NewsAppConfig(AppConfig):
    def ready(self):
        import news_app.signals
```

**What this does:**
- `ready()` - Called when app is loaded
- Import signals to register them with Django

---

## Workflow Summary

### When Article is Approved:

1. **User action:** Editor checks "is_approved" checkbox and saves
2. **pre_save signal fires:** Store old approval status
3. **Article saved to database**
4. **post_save signal fires:**
   - Compare old and new approval status
   - If changed from False to True:
     a. Get all subscribers (publisher + journalist)
     b. Send email to each subscriber
     c. Post to X (if configured)
5. **User sees success message**

---

## Error Handling

### Email Failures
- Each email is in try/except block
- If one fails, others still send
- Errors are logged but don't break approval

### X API Failures
- Check if token is configured
- Use timeout to prevent hanging
- Catch network exceptions
- Log errors but don't break approval

### Why This Matters
- Article approval is the core functionality
- External services (email, X) shouldn't break it
- Graceful degradation: log errors, continue execution

---

## Configuration Required

### In settings.py:
```python
# Email configuration
DEFAULT_FROM_EMAIL = 'noreply@newsapp.com'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Development
# For production:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-password'

# X API configuration
X_BEARER_TOKEN = 'your-x-bearer-token-here'  # Add for production
```

---

## Key Takeaways

1. **Signals decouple logic** - Approval view doesn't need to know about emails/X
2. **pre_save + post_save** work together to detect changes
3. **Sets prevent duplicates** when collecting subscribers
4. **Error handling is crucial** - Don't break approval if email/X fails
5. **Graceful degradation** - Log errors, continue execution
6. **Defensive coding** - Check configuration, handle exceptions
7. **F-strings for readability** - Easy to build dynamic messages
8. **try/except for external services** - Network calls can fail
9. **Print statements for debugging** - See what's happening in console
10. **Signals must be imported** in apps.py to work

---

## Testing Signals

### To test in development:
1. Create a journalist and article
2. Create a reader subscribed to journalist
3. Mark article as approved in admin
4. Check console for email output (EMAIL_BACKEND=console)
5. Check console for X API messages

### Expected Output:
```
Email sent to reader@example.com for article: My Article
X API token not configured. Skipping X post.
```

---

## Production Considerations

1. **Use async tasks** (Celery) for email/X in production
2. **Configure real SMTP** server for actual email delivery
3. **Add X API credentials** to settings (environment variables)
4. **Rate limiting** - X API has rate limits
5. **Queue failed emails** for retry
6. **Monitor signal execution** - Log to file, not console
7. **Use absolute URLs** - Not 127.0.0.1:8000
