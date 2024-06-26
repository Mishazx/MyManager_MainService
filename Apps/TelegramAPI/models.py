from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_init
from django.dispatch import receiver
from django.utils import timezone


class TelegramUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True)
    userid = models.BigIntegerField(null=False)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    image_data = models.BinaryField(null=True, blank=True)
    
class LinkKey(models.Model):
    user = models.OneToOneField(TelegramUser, on_delete=models.CASCADE, null=True)
    token = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)
    
@receiver(post_init, sender=LinkKey)
def delete_expired_keys(sender, instance, **kwargs):
    """Delete expired key pairs."""
    expiration = instance.created_at + timezone.timedelta(minutes=15)
    if timezone.now() > expiration:
        instance.delete()
