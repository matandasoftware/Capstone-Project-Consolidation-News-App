from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Store, Product
from .twitter_utils import tweet_new_store, tweet_new_product, delete_tweet
import logging
import threading

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Store)
def handle_store_created(sender, instance, created, **kwargs):
    """
    Automatically tweet when a new store is created.
    
    Args:
        sender: Store model class
        instance: The actual store object that was saved
        created: True if this is a new store, False if it's an update
    """
    if created:
        def tweet_in_background():
            try:
                tweet_new_store(instance)
            except Exception as e:
                logger.error(f"Error tweeting new store: {e}")
        
        thread = threading.Thread(target=tweet_in_background)
        thread.daemon = True
        thread.start()


@receiver(post_save, sender=Product)
def handle_product_created(sender, instance, created, **kwargs):
    """
    Automatically tweet when a product is created or updated.
    - New product: Tweet announcement with image
    - Updated product: Delete old tweet, post new one with updated image
    """
    def tweet_in_background():
        if created:
            try:
                tweet_new_product(instance)
            except Exception as e:
                logger.error(f"Error tweeting new product: {e}")
        else:
            try:
                from .twitter_utils import tweet_updated_product
                tweet_updated_product(instance)
            except Exception as e:
                logger.error(f"Error tweeting updated product: {e}")
    
    thread = threading.Thread(target=tweet_in_background)
    thread.daemon = True
    thread.start()


@receiver(pre_delete, sender=Store)
def handle_store_deleted(sender, instance, **kwargs):
    """Delete the associated tweet when a store is deleted."""
    if instance.tweet_id:
        def delete_in_background():
            try:
                delete_tweet(instance.tweet_id)
                logger.info(f"Deleted tweet for store: {instance.name}")
            except Exception as e:
                logger.error(f"Error deleting store tweet: {e}")
        
        thread = threading.Thread(target=delete_in_background)
        thread.daemon = True
        thread.start()


@receiver(pre_delete, sender=Product)
def handle_product_deleted(sender, instance, **kwargs):
    """Delete the associated tweet when a product is deleted."""
    if instance.tweet_id:
        def delete_in_background():
            try:
                delete_tweet(instance.tweet_id)
                logger.info(f"Deleted tweet for product: {instance.name}")
            except Exception as e:
                logger.error(f"Error deleting product tweet: {e}")
        
        thread = threading.Thread(target=delete_in_background)
        thread.daemon = True
        thread.start()