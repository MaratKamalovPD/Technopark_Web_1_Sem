from __future__ import unicode_literals
from django.db import models
from .users import *
from .likes import *
from .questions import *

like_choices = (
    ('q', 'question'),
    ('a', 'answer'),
    ('u', 'user')
)


class LikesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()



class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', default=None)
    type = models.CharField(choices=like_choices, max_length=1)



    manager = LikesManager()