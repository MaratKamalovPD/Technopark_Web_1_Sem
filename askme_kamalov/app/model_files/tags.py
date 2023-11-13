from __future__ import unicode_literals
from django.db import models
from .users import *

class TagsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    manager = TagsManager()

    def __str__(self):
        return self.name