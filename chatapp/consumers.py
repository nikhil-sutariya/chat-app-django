import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chatapp.models import Conversation, Message 
from channels.db import database_sync_to_async
from users.models import User
from chatapp.chatapp_api_v1.serializers import MessageSerializer
from asgiref.sync import sync_to_async

# websocket url
# ws://127.0.0.1:8000/chat/9876543210-9876543212?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAzMzEyMjk5LCJpYXQiOjE3MDA3MjAyOTksImp0aSI6ImFhNGZhZDIxN2UzMTQ5ZDBiYWNhZjExZDEwZjc3YjFjIiwidXNlcl9pZCI6IjNmNWRiZTMwLWE3MDYtNGUyYi04ODRmLTNkMjI5MjU4YmVmNCJ9.d-fitmZak4sW7JtZ6JzAl5coP_zIAz_aJd-hEckP8Mk

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = self.scope["user"]
        
        room_name = self.scope["url_route"]["kwargs"]["room_name"]
        if room_name.split('-')[0] == sender.phone:
            receiver_phone = room_name.split('-')[1]
        else:
            receiver_phone = room_name.split('-')[0]
        receiver = await self.get_user(receiver_phone)
        
        conversation_data = {
            "room_name": room_name,
            "sender": sender, 
            "receiver": receiver
        }
        conversation = await self.get_or_create_conversation(conversation_data)

        message_data = {
            "conversation": conversation, 
            "sender": sender, 
            "receiver": receiver, 
            "message": message
        }
        message_obj = await self.create_message(message_data)
        await self.channel_layer.group_send(self.room_group_name, {"type": "chat.message", "message": message_obj})

    async def chat_message(self, event):
        message = await self.get_message(event["message"])
        if message: await self.send(text_data=json.dumps({"message": message}))
        else: await self.send(text_data=json.dumps({"error_message": "Something went wrong"}))

    @database_sync_to_async
    def get_user(self, phone):
        try:
            user = User.objects.get(phone=phone)
            return user
        except:
            return None
        
    @database_sync_to_async
    def get_or_create_conversation(self, data):
        try:
            conversation, created = Conversation.objects.get_or_create(room_name=data['room_name'], sender=data['sender'], receiver=data['receiver'])
            return conversation
        except:
            return None

    @database_sync_to_async
    def create_message(self, data):
        try:
            message = Message.objects.create(conversation=data['conversation'], sender=data['sender'], receiver=data['receiver'], message=data['message'])
            return message
        except Exception as e:
            print(e)
            return None

    @database_sync_to_async
    def get_message(self, message_obj):
        try:
            serializer = MessageSerializer(message_obj)
            return serializer.data
        except:
            return None