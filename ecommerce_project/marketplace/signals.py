# Auto-tweet when stores and products are created

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Store, Product
from .twitter_service import twitter_service


@receiver(post_save, sender=Store)
def tweet_new_store(sender, instance, created, **kwargs):
    if created:
        print(f"New store created: {instance.name}. Sending tweet...")
        twitter_service.tweet_new_store(instance)


@receiver(post_save, sender=Product)
def tweet_new_product(sender, instance, created, **kwargs):
    if created:
        print(f"New product created: {instance.name}. Sending tweet...")
        twitter_service.tweet_new_product(instance)
