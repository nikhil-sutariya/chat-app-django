import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chatapp.models import Conversation, Message 
from channels.db import database_sync_to_async
from users.models import User
from chatapp.chatapp_api_v1.serializers import MessageSerializer

# websocket url
# ws://127.0.0.1:8000/chat/9408016008-9876543212?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUzMTYxNTQyLCJpYXQiOjE3MjE2MjU1NDIsImp0aSI6ImY5MTgwMzJkYTBhZjRlYTdiYTQ4MGRmN2E2ZjI1YTFkIiwidXNlcl9pZCI6IjM3Y2Q3NTJmLTQ1MjMtNDI1Yi1hMzQ0LTM1ODJkYzViNGQ4YSJ9.S-dpkulyqIdZDyHhqmgYq_Y0sAcm9qIMSSCKWmvHbUg

class ChatConsumer(AsyncWebsocketConsumer):
    async def get_room_name(self, sender_phone, receiver_phone):
        phones = sorted([sender_phone, receiver_phone])
        return "-".join(phones)
    
    async def check_room(self, event):
        channel = event["channel"]
        await self.send(channel, {'type': 'room_exists'})

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        sender_phone = self.room_name.split("-")[0]
        receiver_phone = self.room_name.split("-")[1]
    
        self.room_name = await self.get_room_name(sender_phone, receiver_phone)
        self.room_group_name = f"chat_{self.room_name}"

        # Check if room already exists
        await self.channel_layer.group_send(self.room_name, {'type': 'check_room'})
        
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

        room_name = await self.get_room_name(sender.phone, receiver_phone)
        
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
            room_name = data['room_name']
            conversations = Conversation.objects.filter(room_name=room_name)

            if conversations.exists():
                conversation = conversations.first()

            else:
                conversation = Conversation(room_name=data['room_name'], sender=data['sender'], receiver=data['receiver'])
                conversation.save()

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