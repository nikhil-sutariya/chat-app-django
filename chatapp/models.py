from django.db import models
from users.models import User

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)