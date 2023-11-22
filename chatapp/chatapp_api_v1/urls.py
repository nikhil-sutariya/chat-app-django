from django.urls import path
from chatapp.chatapp_api_v1.views import FetchUsersAPIView

urlpatterns = [
    path('fetch-users', FetchUsersAPIView.as_view(), name ='fetch-user')
]
