from django.urls import path
from users.users_api_v1.views import RegisterPhoneAPIView, LogoutAPIView, \
    UserListAPIView, UserDetailsAPIView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('phone-register-login', RegisterPhoneAPIView.as_view(), name ='phone-register-login'),
    path('login/refresh', jwt_views.TokenRefreshView.as_view(), name ='token-refresh'),
    path('logout', LogoutAPIView.as_view(), name = 'logout-user'),
    path('user/<str:id>', UserDetailsAPIView.as_view(), name = 'user-details'),    
    path('admin/users', UserListAPIView.as_view(), name = 'users-list'),
]
