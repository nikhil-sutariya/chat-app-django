from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from users.users_api_v1.serializers import UserSerializer
from django.db.models import Q
from chatapp.chatapp_api_v1.serializers import MessageSerializer
from chatapp.models import Message
from chatapp import response as chat_app_response

class FetchUsersAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def get(self, request):
        try:
            user = self.request.user
            users = User.objects.filter(~Q(pk=user.pk) & Q(is_superuser=False))
            serializer = self.serializer_class(users, many=True, context={"request": request})

            response = {
                "success": True,
                "count": users.count(),
                "message": chat_app_response.contact_list,
                "data": serializer.data
            }
        
        except Exception as e:
            response = {
                "success": True,
                "message": chat_app_response.error_message,
                "error_message": str(e),
                "data": None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(response, status=status.HTTP_200_OK)
    
class FetchConversationAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = MessageSerializer

    def get(self, request):
        try:
            user = self.request.user
            messages = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('timestamp')
            serializer = self.serializer_class(messages, many=True, context={"request": request})

            response = {
                "success": True,
                "message": chat_app_response.chat_history,
                "data": serializer.data
            }
        
        except Exception as e:
            response = {
                "success": False,
                "message": chat_app_response.error_message,
                "error_message": str(e),
                "data": None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(response, status=status.HTTP_200_OK)
