from django.urls import path
from chatapp.consumers import ChatConsumer

'''
    Room will become sender's_phone-receiver's_phone
    and the websocket url is ws://domain.com/sender's_phone-receiver's_phone?token=loggedin_user's_token
    e.g - ws://127.0.0.1:8000/chat/9876543210-9876543212?token=insert_jwt_token_here
'''

websocket_urlpatterns = [
    path('chat/<str:room_name>', ChatConsumer.as_asgi()),
]
