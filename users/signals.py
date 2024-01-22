from django.db.models.signals import pre_save
from django.dispatch import receiver
from users.models import User
from app.global_helper import generate_key_pair

@receiver(pre_save, sender=User)
def store_public_private_keys(sender, instance, raw, **kwargs):
    if not instance.public_key or not instance.private_key:
        keys = generate_key_pair()
        instance.public_key = keys['public_key']
        instance.private_key = keys['private_key'] 
