import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chatapp.models import Conversation, Message 
from channels.db import database_sync_to_async
from users.models import User

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
        conversation = await self.get_or_create_conversation(room_name)
        
        data = {
            "conversation": conversation, 
            "sender": sender, 
            "receiver": receiver, 
            "message": message
        }
        await self.create_message(data)
        await self.channel_layer.group_send(self.room_group_name, {"type": "chat.message", "message": message})

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def get_user(self, phone):
        try:
            user = User.objects.get(phone=phone)
            return user
        except:
            return None
        
    @database_sync_to_async
    def get_or_create_conversation(self, room_name):
        try:
            conversation, created = Conversation.objects.get_or_create(room_name=room_name)
            return conversation
        except:
            return None

    @database_sync_to_async
    def create_message(self, data):
        try:
            message = Message.objects.create(conversation=data['conversation'], sender=data['sender'], receiver=data['receiver'], message=data['message'])
            return message
        except:
            return None
