from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    avatar = models.ImageField(upload_to='img/users/', null=True, blank=True, default="avatar.jpeg")