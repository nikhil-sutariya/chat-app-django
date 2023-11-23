from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from chatapp.models import Conversation, Message
from app.global_helper import encrypt_message, generate_key_pair

@receiver(post_save, sender=Conversation)
async def store_public_private_keys(sender, instance, created, **kwargs):
    if created:
        print("From signals")
        keys = await generate_key_pair()
        print(keys)
        instance.public_key = keys['public_key']
        instance.private_key = keys['private_key'] 
        instance.save()

@receiver(pre_save, sender=Message)
def encrypt_conversation_message(sender, instance, raw, **kwargs):
    cipher_text = encrypt_message(instance.message, instance.conversation.public_key)
    instance.message = cipher_text
    instance.save()
