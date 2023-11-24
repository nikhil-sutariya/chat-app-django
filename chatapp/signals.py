from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from chatapp.models import Conversation, Message
from app.global_helper import encrypt_message, generate_key_pair

@receiver(pre_save, sender=Conversation)
def store_public_private_keys(sender, instance, raw, **kwargs):
    if not instance.public_key or not instance.private_key:
        keys = generate_key_pair()
        instance.public_key = keys['public_key']
        instance.private_key = keys['private_key'] 

@receiver(pre_save, sender=Message)
def encrypt_conversation_message(sender, instance, raw, **kwargs):
    cipher_text = encrypt_message(instance.message, instance.conversation.public_key)
    instance.message = cipher_text
