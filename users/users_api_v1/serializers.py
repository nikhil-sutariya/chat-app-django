from rest_framework.serializers import ModelSerializer, Serializer, CharField, EmailField, ImageField, IntegerField
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils import timezone
from users import response as users_app_response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout

class UserSerializer(ModelSerializer):
    profile_picture = ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name','last_name', 'phone', 'email', 'profile_picture', 'bio', 'is_active']

class RegisterPhoneSerializer(ModelSerializer):
    email = CharField(max_length=100, required=False)
    phone = IntegerField(required=True)
    profile_picture = ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone', 'email', 'profile_picture']

    def create(self, validated_data):
        phone = validated_data.get('phone')
        if User.objects.filter(phone=phone).exists():
            user = User.objects.get(phone=phone)
            return user
        return User.objects.create_user(**validated_data)
    
    def to_representation(self, instance):
        request = self.context.get('request')
        refresh = RefreshToken.for_user(instance)
        login(request, instance)

        data = super().to_representation(instance)
        data['refreshToken'] = str(refresh)
        data['accessToken'] = str(refresh.access_token)
        return data

class LogoutSerializer(Serializer):
    refresh = CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        
        except TokenError:
            self.fail(users_app_response.error_message)
