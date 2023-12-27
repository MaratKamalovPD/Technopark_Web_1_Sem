from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import models
from django.forms import ImageField
from app.model_files.questions import Question
from . import models
from .model_files.answers import Answer
from .model_files.tags import Tag


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']
        username = self.cleaned_data['username']
        if data == 'wrongpass':
            raise ValidationError('Wrong password')
        return data

class RegisterForm(forms.ModelForm):
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = get_user_model()
        #model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        username = self.cleaned_data['username']

        if password != password_check:
            raise ValidationError('Passwords do not match')
        if get_user_model().objects.filter(username=username).exists():
            raise ValidationError('Such a user already exists')

    def save(self, **kwargs):
        self.cleaned_data.pop('password_check')
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exists():
            return
        else:
            return get_user_model().objects.create_user(**self.cleaned_data)

class AskQuestionForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            self.user_id = kwargs.pop('user_id', None)
            super(AskQuestionForm, self).__init__(*args, **kwargs)

        title = forms.CharField(min_length=5)
        text = forms.CharField(widget=forms.Textarea)
        tags = forms.CharField()

        class Meta:
            model = Question
            # model = User
            fields = ['title', 'text', 'tags']

        def clean(self):
            title = self.cleaned_data['title']
            text = self.cleaned_data['text']
            tags = self.cleaned_data['tags']


            if 'aaa' in title:
                raise ValidationError('The use of profanity is prohibited')
            # if Question.objects.filter(title=title).exists():
            #     raise ValidationError('Such a question already exists')

        def save(self, **kwargs):
            title = self.cleaned_data['title']
            text = self.cleaned_data['text']

            question = Question(title=title, text=text, owner_id = self.user_id)
            question.save()

            tags = self.cleaned_data['tags']
            words = tags.split(",")
            for i in range(len(words)):
                tag_exist = models.Tag.manager.get_exist_by_tag(words[i])
                try:
                    print(tag_exist[0])
                    tag = tag_exist[0]
                    question.tags.add(tag)
                except:
                    tag = Tag(name=words[i])
                    tag.save()
                    question.tags.add(tag)
            # tag = Tag(name = 'bibki')
            # tag.save()
            question.save()
            #question.tags.add(tag)


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        self.question_id = kwargs.pop('question_id', None)
        super(AnswerForm, self).__init__(*args, **kwargs)

    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Answer
        # model = User
        fields = ['content']

    def clean(self):
        content = self.cleaned_data['content']


        if 'aaa' in content:
            raise ValidationError('The use of profanity is prohibited')
        # if Question.objects.filter(title=title).exists():
        #     raise ValidationError('Such a question already exists')

    def save(self, **kwargs):
        content = self.cleaned_data['content']


        answer = Answer(content=content, checked=False, likes_count = 0, question_id = self.question_id, user_creator_id=self.user_id)
        answer.save()

class SettingsForm(forms.ModelForm):
    avatar = ImageField(required=False)
    first_name = forms.CharField(min_length=4, widget=forms.TextInput)
    last_name = forms.CharField(widget=forms.TextInput)
    email = forms.CharField(widget=forms.TextInput)
    class Meta:
        model = get_user_model()
        #model = User
        fields = ['first_name', 'last_name', 'email', 'avatar']

    # def clean(self):
    #     password = self.cleaned_data['password']
    #     password_check = self.cleaned_data['password_check']
    #     username = self.cleaned_data['username']
    #
    #     if password != password_check:
    #         raise ValidationError('Passwords do not match')
    #     if get_user_model().objects.filter(username=username).exists():
    #         raise ValidationError('Such a user already exists')
    #
    def save(self, **kwargs):
        user = super().save(**kwargs)
        user.avatar = self.cleaned_data.get('avatar')
        return user