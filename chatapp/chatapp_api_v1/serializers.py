from rest_framework.serializers import ModelSerializer
from chatapp.models import Conversation, Message
from users.users_api_v1.serializers import UserSerializer
from app.global_helper import date_formatting, decrypt_message, get_time

class ConversationSerializer(ModelSerializer):
    sender = UserSerializer(many=False, read_only=True)
    receiver = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'room_name', 'sender', 'receiver', 'timestamp']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        last_message = Message.objects.filter(conversation=instance).values('message').last()
        if last_message:
            data['last_massage'] = decrypt_message(last_message['message'], instance.private_key)
        data['timestamp'] = date_formatting(data['timestamp'])
        return data

class MessageSerializer(ModelSerializer):
    conversation = ConversationSerializer(many=False, read_only=True)
    sender = UserSerializer(many=False, read_only=True)
    receiver = UserSerializer(many=False, read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['message'] = decrypt_message(instance.message, instance.conversation.private_key)
        data['sender']['name'] = f"{data['sender']['first_name']} {data['sender']['last_name']}"
        data['receiver']['name'] = f"{data['receiver']['first_name']} {data['receiver']['last_name']}"
        del data['sender']['is_active']
        del data['sender']['first_name']
        del data['sender']['last_name']
        del data['receiver']['is_active']
        del data['receiver']['first_name']
        del data['receiver']['last_name']
        data['date'] = date_formatting(data['timestamp'])
        data['time'] = get_time(data['timestamp'])
        del data['timestamp']
        return data 
