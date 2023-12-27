from django.contrib import auth
from django.contrib.auth import login, authenticate, login as dj_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpRequest
from django.views.decorators.csrf import csrf_protect

from . import models
from .forms import *
from .model_files.questions import Question

PER_PAGE = 5
# QUESTIONS = [
#         {
#             'id': i,
#             'title': f'Question {i}',
#             'text': f'Text {i}'
#         } for i in range(40)
#    ]

QUESTIONS = models.Question.manager.get_queryset()

def paginate(objects, page, per_page=PER_PAGE):
    paginator = Paginator(objects, per_page)
    page_items = paginator.page(1).object_list
    return paginator.get_page(page)

# Create your views here.

def index(request):
    page = request.GET.get('page', 1)
    mod = request.GET.get('mod', 'new')
    if mod == 'new':
        questions = models.Question.manager.get_new()
    if mod == 'hot':
        questions = models.Question.manager.get_hot()
    pages = len(questions) // PER_PAGE
    return render(request, template_name='index.html', context= { 'questions': paginate(questions, page= page), 'pages': range(1, pages + 1), 'cur_page': str(page)})


def question(request):
    # pk = request.GET.get('answer_page', None)
    # if pk == None:
    #      return render(request, 'ask.html')
    question_id = int(request.GET.get('id'))

    if request.method == "GET":
        answer_form = AnswerForm()
    if request.method == "POST":
        answer_form = AnswerForm(request.POST, user_id = request.user.id, question_id = question_id)
        if answer_form.is_valid():
            answer_form.save()
            str_url = 'http://127.0.0.1:8000/question?id=%s' % question_id
            print(str_url)
            return redirect(str_url)


    try:
        question = models.Question.manager.get(id=question_id)
    except models.Question.DoesNotExist:
        raise Http404("Question not found")

    question_item = QUESTIONS[question_id-1]
    page = request.GET.get('page', 1)

    answers = question.answers.all()
    pages = len(answers) // PER_PAGE
    return render(request, template_name='question.html', context= { 'question': question_item , 'answers': paginate(answers, page= page),'pages': range(1, pages + 1), 'cur_page': page, "form": answer_form})


def registration(request):
    if request.method == "GET":
        user_form = RegisterForm()
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                return redirect(reverse('login'))
            else:
                user_form.add_error(field=None, error="Registration failed!")

    return (render(request, template_name="registration.html", context={"form": user_form}))

def log_in(request):
    return render(request, template_name='login.html')

def auth(request):
    return render(request, template_name='auth-box.html')

@login_required
def ask(request):
    if request.method == "GET":
        ask_form = AskQuestionForm()
    if request.method == "POST":
        ask_form = AskQuestionForm(request.POST, user_id = request.user.id)
        if ask_form.is_valid():
            ask_form.save()
            number = models.Question.manager.get_count()
            str_url = 'http://127.0.0.1:8000/question?id=%s' % number
            print(str_url)
            return redirect(str_url)


    return (render(request, template_name="ask.html", context={"form": ask_form}))

@csrf_protect
@login_required
def settings(request):
    if request.method == "GET":
        settings_form = SettingsForm(initial=model_to_dict(request.user))
    if request.method == "POST":
        settings_form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if settings_form.is_valid():
            settings = settings_form.save()
            return redirect(reverse('settings'))


    return (render(request, template_name="settings.html", context={"form": settings_form}))


def tag(request, tag):
    page = request.GET.get('page', 1)
    tag_instance = models.Tag.manager.get(name=tag)
    questions = tag_instance.questions.order_by('-likes_count', '-create_data', 'title')
    pages = len(questions) // PER_PAGE

    return render(request, template_name='tag.html', context= {'tag': tag_instance, 'questions': questions})

@csrf_protect
def login(request):
    if request.method == "GET":
        login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            #username = request.POST.get('username', None)
            #password = request.POST.get('password', None)
            user = authenticate(**login_form.cleaned_data)
            if user is not None:
                dj_login(request, user)
                return redirect(reverse('index'))
            else:
                login_form.add_error(field=None, error="Wrong password or user does not exist")

    return (render(request, template_name="login.html", context={"form": login_form}))

def logout_function(request):
    logout(request)
    return redirect(reverse('index'))

def signup(request):
    return
