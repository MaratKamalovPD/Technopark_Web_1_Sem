import django.contrib.admin
from django.contrib import admin

# Register your models here.
from .model_files.questions import *
from .model_files.answers import *
from .model_files.likes import *
from .model_files.tags import *
from .model_files.users import *

admin.site.register(Answer)
admin.site.register(Like)
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(User)