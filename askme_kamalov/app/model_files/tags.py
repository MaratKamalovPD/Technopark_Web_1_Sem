from __future__ import unicode_literals
from django.db import models
from .users import *

class TagsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()
    def get_exist_by_tag(self, tag_name):
        return super().get_queryset().filter(name = tag_name)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    manager = TagsManager()

    def __str__(self):
        return self.name