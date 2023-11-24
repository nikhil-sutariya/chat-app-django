from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
import uuid

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_name = models.CharField(_('room name'), max_length=100)
    private_key = models.TextField(null=True, blank=True)
    public_key = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "conversation"
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"

    def __str__(self):
        return self.room_name

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(_('message'), max_length=10000)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "message"
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"Message from {self.sender.first_name} {self.sender.last_name} to {self.receiver.first_name} {self.receiver.last_name}"
