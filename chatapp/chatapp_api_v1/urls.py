from django.urls import path
from chatapp.chatapp_api_v1.views import FetchUsersAPIView, FetchConversationAPIView

urlpatterns = [
    path('fetch-users', FetchUsersAPIView.as_view(), name ='fetch-user'),
    path('fetch-conversation', FetchConversationAPIView.as_view(), name='fetch-conversation')
]
