from django.contrib import admin
from chatapp.models import Conversation, Message

admin.site.register(Conversation)
admin.site.register(Message)