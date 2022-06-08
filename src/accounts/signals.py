from .models import Account
from django.db.models.signals import post_save
from django.dispatch import receiver
from carts.models import Cart

@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(cart_id=instance)
