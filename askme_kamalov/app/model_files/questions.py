from __future__ import unicode_literals
from django.db import models
from .users import *
from .tags import *
from .likes import *

class QuestionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()

    def get_new(self):
        return super().get_queryset().order_by('-create_data')

    def get_hot(self):
        return super().get_queryset().order_by('-likes_count')

    def get_by_tag(self, tag_name):
        return Tag.manager.get(name=tag_name).questions.all()

    def like_it(self, instance, user):
        try:
            like = instance.likes.get(owner=user)
            instance.likes.remove(like)
            instance.likes_count -= 1
            instance.save()
            return False
        except BaseException:
            like = Like.manager.create(owner=user, type='q')
            instance.likes.add(like)
            instance.likes_count += 1
            instance.save()
            return True

class Question(models.Model):
    owner = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='questions')
    likes = models.ManyToManyField(Like)
    likes_count = models.IntegerField(default=0)
    create_data = models.DateTimeField(auto_now_add=True)

    manager = QuestionManager()