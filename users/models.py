from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid
from users.manager import UserManager

class User(AbstractUser):    
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique= True, blank=True, null=True)
    phone = models.CharField(_('phone number'), max_length= 10, unique= True)
    profile_picture = models.ImageField(_('profile picture'), upload_to='profile_pictures', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        db_table = "users"
        verbose_name = "Users"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.phone

