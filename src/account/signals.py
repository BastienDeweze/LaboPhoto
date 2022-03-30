from .models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Code

@receiver(post_save, sender=CustomUser)
def create_create_user(sender, instance, created, **kwargs):
    if created:
        
        Code.objects.create(user=instance)
        instance.code.refresh_code()
        instance.code.save()