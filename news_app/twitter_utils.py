import tweepy
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def get_twitter_client():
    """Initialize and return Twitter API client for posting tweets."""
    api_key = settings.TWITTER_API_KEY
    api_secret = settings.TWITTER_API_SECRET
    access_token = settings.TWITTER_ACCESS_TOKEN
    access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
    
    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("⚠️ Twitter API credentials not configured")
        logger.warning("Twitter API credentials not configured")
        return None
    
    try:
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        api.verify_credentials()
        print("✅ Twitter API authentication successful")
        logger.info("Twitter API authentication successful")
        return api
    except tweepy.TweepyException as e:
        print(f"❌ Twitter API authentication failed: {e}")
        logger.error(f"Twitter API authentication failed: {e}")
        return None


def tweet_article(article):
    """Post a tweet announcing an approved article."""
    if not settings.TWITTER_ENABLED:
        print("ℹ️ Twitter integration is disabled")
        logger.info("Twitter integration is disabled")
        return None
    
    print(f"🐦 Attempting to tweet article: {article.title}")
    api = get_twitter_client()
    if not api:
        print("❌ Failed to get Twitter client")
        return None
    
    try:
        # Build article URL
        article_url = f"http://127.0.0.1:8000/article/{article.slug}/"
        
        # Build tweet text
        tweet_text = f"📰 New Article Published!\n\n"
        tweet_text += f"{article.title}\n\n"
        
        # Add summary (truncate if too long)
        if len(article.summary) > 100:
            tweet_text += f"{article.summary[:100]}...\n\n"
        else:
            tweet_text += f"{article.summary}\n\n"
        
        tweet_text += f"Read more: {article_url}\n\n"
        
        # Add hashtags
        if article.publisher:
            publisher_tag = article.publisher.name.replace(' ', '')
            tweet_text += f"#{publisher_tag} #News"
        else:
            tweet_text += "#IndependentJournalism #News"
        
        # Post tweet
        print(f"📤 Posting tweet:\n{tweet_text}")
        tweet = api.update_status(tweet_text)
        print(f"✅ Tweet posted successfully! Tweet ID: {tweet.id}")
        logger.info(f"Tweet posted for article {article.title}: {tweet.id}")
        return tweet
    except tweepy.TweepyException as e:
        print(f"❌ Failed to tweet article: {e}")
        logger.error(f"Failed to tweet article: {e}")
        return None
