from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from users.users_api_v1.serializers import RegisterPhoneSerializer, LogoutSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from users.models import User
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser
from app.exceptions import ObjectExists
import os
from users import response as users_app_response
from app import global_helper

live_url = os.getenv('LIVE_URL')

class RegisterPhoneAPIView(GenericAPIView):
    serializer_class = RegisterPhoneSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data = data, context = {"request": request})
            serializer.is_valid(raise_exception = True)
            serializer.save()
            
            response = {
                "success": True,
                "message": users_app_response.user_logged_in,
                "data": serializer.data
            }
        
        except Exception as e:
            response = {
                "success": False,
                "message": users_app_response.error_message,
                "error_message": str(e),
                "data": None
            }

            return Response(response, status = status.HTTP_400_BAD_REQUEST)
        
        return Response(response, status = status.HTTP_201_CREATED)

class LogoutAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            logout(request)
            response = {
                'success': True,
                'message': users_app_response.user_logged_out,
                'data': None
            }

        except Exception as e:
            response = {
                "success": False,
                "message": users_app_response.error_message,
                "error_message": str(e),
                "data": None
            }
            return Response(response, status = status.HTTP_400_BAD_REQUEST)
    
        return Response(response, status= status.HTTP_200_OK)

class UserDetailsAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(request.user)
            response = {
                "success": True,
                "message": users_app_response.user_data,
                "data": serializer.data
            }

        except Exception as e:
            response = {
                "success": False,
                "message": users_app_response.error_message,
                "error_message": str(e),
                "data": None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        return Response(response, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        try:
            user = request.user
            data = request.data
            serializer = self.serializer_class(user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            response = {
                'success': True,
                'message': users_app_response.profile_updated,
                'data': serializer.data
            }

        except Exception as e:
            response = {
                'success': False,
                'message': users_app_response.error_message,
                'error_message': str(e),
                'data': None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
        return Response(response, status=status.HTTP_200_OK)

""" Admin APIs """
class UserListAPIView(GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name','last_name']
    ordering_fields = '__all__'
    
    def get(self, request):
        try:
            users = global_helper.get_or_raise(User, obj_id=None, error_message=None)
            serializer = self.serializer_class(users, many=True)
            response = {
                "success": True,
                "message": users_app_response.getting_users,
                "data": serializer.data
            }

        except Exception as e:
            response = {
                "success": False,
                "message": users_app_response.error_message,
                "error_message": str(e),
                "data": None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(response, status=status.HTTP_200_OK)
