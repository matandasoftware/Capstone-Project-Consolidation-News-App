import tweepy
from django.conf import settings
import logging
import os

logger = logging.getLogger(__name__)


def get_twitter_client():
    """Initialize and return Twitter API v2 client with OAuth 1.0a."""
    api_key = settings.TWITTER_API_KEY
    api_secret = settings.TWITTER_API_SECRET
    access_token = settings.TWITTER_ACCESS_TOKEN
    access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
    
    if not all([api_key, api_secret, access_token, access_token_secret]):
        logger.warning("Twitter API credentials not configured")
        return None
    
    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        logger.info("Twitter API v2 client initialized")
        return client
    except Exception as e:
        logger.error(f"Twitter API client initialization failed: {e}")
        return None


def get_twitter_api_v1():
    """Initialize Twitter API v1.1 for media upload."""
    api_key = settings.TWITTER_API_KEY
    api_secret = settings.TWITTER_API_SECRET
    access_token = settings.TWITTER_ACCESS_TOKEN
    access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET
    
    if not all([api_key, api_secret, access_token, access_token_secret]):
        return None
    
    try:
        auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
        api = tweepy.API(auth)
        return api
    except Exception as e:
        logger.error(f"Twitter API v1.1 initialization failed: {e}")
        return None


def delete_tweet(tweet_id):
    """Delete a tweet by ID."""
    if not tweet_id:
        return False
    
    client = get_twitter_client()
    if not client:
        return False
    
    try:
        client.delete_tweet(tweet_id)
        logger.info(f"Deleted old tweet: {tweet_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to delete tweet {tweet_id}: {e}")
        return False


def tweet_new_store(store):
    """Post a tweet announcing a new store."""
    if not settings.TWITTER_ENABLED:
        logger.info("Twitter integration is disabled")
        return None
    
    client = get_twitter_client()
    if not client:
        return None
    
    try:
        tweet_text = f"🏪 NEW STORE: {store.name}\n\n"
        tweet_text += f"{store.description}\n\n"
        tweet_text += "#eCommerce #NewStore"
        
        response = client.create_tweet(text=tweet_text)
        tweet_id = response.data['id']
        logger.info(f"Tweet posted for store {store.name}: {tweet_id}")
        
        store.tweet_id = tweet_id
        store.save(update_fields=['tweet_id'])
        
        return response
    except Exception as e:
        logger.error(f"Failed to tweet new store: {e}")
        return None


def tweet_new_product(product):
    """Post a tweet announcing a new product with image."""
    if not settings.TWITTER_ENABLED:
        return None
    
    client = get_twitter_client()
    if not client:
        return None
    
    try:
        tweet_text = f"🆕 NEW PRODUCT: {product.name}\n"
        tweet_text += f"Available at: {product.store.name}\n\n"
        
        if len(product.description) > 100:
            tweet_text += f"{product.description[:100]}...\n\n"
        else:
            tweet_text += f"{product.description}\n\n"
        
        tweet_text += f"💰 Price: ${product.price}\n#Product #Shopping"
        
        media_id = None
        if product.image and hasattr(product.image, 'path') and os.path.exists(product.image.path):
            api_v1 = get_twitter_api_v1()
            if api_v1:
                try:
                    media = api_v1.media_upload(product.image.path)
                    media_id = media.media_id
                    logger.info(f"Product image uploaded")
                except Exception as e:
                    logger.warning(f"Image upload failed: {e}")
        
        if media_id:
            response = client.create_tweet(text=tweet_text, media_ids=[media_id])
        else:
            response = client.create_tweet(text=tweet_text)
        
        tweet_id = response.data['id']
        logger.info(f"Tweet posted for product {product.name}: {tweet_id}")
        
        product.tweet_id = tweet_id
        product.save(update_fields=['tweet_id'])
        
        return response
    except Exception as e:
        logger.error(f"Failed to tweet new product: {e}")
        return None


def tweet_updated_product(product):
    """Delete old tweet and post new one with updated image."""
    if not settings.TWITTER_ENABLED:
        return None
    
    if product.tweet_id:
        delete_tweet(product.tweet_id)
    
    client = get_twitter_client()
    if not client:
        return None
    
    try:
        tweet_text = f"🆕 NEW PRODUCT: {product.name}\n"
        tweet_text += f"Available at: {product.store.name}\n\n"
        
        if len(product.description) > 100:
            tweet_text += f"{product.description[:100]}...\n\n"
        else:
            tweet_text += f"{product.description}\n\n"
        
        tweet_text += f"💰 Price: ${product.price}\n#Product #Shopping"
        
        media_id = None
        if product.image and hasattr(product.image, 'path') and os.path.exists(product.image.path):
            api_v1 = get_twitter_api_v1()
            if api_v1:
                try:
                    media = api_v1.media_upload(product.image.path)
                    media_id = media.media_id
                    logger.info(f"Updated image uploaded")
                except Exception as e:
                    logger.warning(f"Image upload failed: {e}")
        
        if media_id:
            response = client.create_tweet(text=tweet_text, media_ids=[media_id])
        else:
            response = client.create_tweet(text=tweet_text)
        
        tweet_id = response.data['id']
        logger.info(f"Updated tweet posted: {tweet_id}")
        
        product.tweet_id = tweet_id
        product.save(update_fields=['tweet_id'])
        
        return response
    except Exception as e:
        logger.error(f"Failed to tweet updated product: {e}")
        return None