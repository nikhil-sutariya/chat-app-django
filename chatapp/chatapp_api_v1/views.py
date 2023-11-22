from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from users.users_api_v1.serializers import UserSerializer
from django.db.models import Q

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
                "message": "Available users.",
                "data": serializer.data
            }
        
        except Exception as e:
            response = {
                "success": True,
                "message": "Something went wrong.",
                "error_message": str(e),
                "data": None
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(response, status=status.HTTP_200_OK)