from __future__ import unicode_literals
from django.db import models
from .users import *
from .likes import *
from .questions import *

class AnswersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()

class Answer(models.Model):
    user_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    checked = models.BooleanField(default=False)
    likes = models.ManyToManyField(Like)
    likes_count = models.IntegerField(default=0)

    manager = AnswersManager()