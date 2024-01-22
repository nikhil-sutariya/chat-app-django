from django.db.models.signals import pre_save
from django.dispatch import receiver
from chatapp.models import Message
from app.global_helper import encrypt_message

@receiver(pre_save, sender=Message)
def encrypt_conversation_message(sender, instance, raw, **kwargs):
    cipher_text = encrypt_message(instance.message, instance.receiver.public_key)
    instance.message = cipher_text
