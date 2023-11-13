from django.shortcuts import render
from django.core.paginator import Paginator
from . import models

PER_PAGE = 5
# QUESTIONS = [
#         {
#             'id': i,
#             'title': f'Question {i}',
#             'text': f'Text {i}'
#         } for i in range(40)
#    ]

QUESTIONS = models.Question.manager.get_queryset()
ANSWERS = [
        {
            'id': i,
            'text': f'Answer {i}'
        } for i in range(15)
    ]
def paginate(objects, page, per_page=PER_PAGE):
    paginator = Paginator(objects, per_page)
    page_items = paginator.page(1).object_list
    return paginator.page(page)

# Create your views here.
def index(request):
    page = request.GET.get('page', 1)
    mod = request.GET.get('mod', 'new')
    if mod == 'new':
        questions = models.Question.manager.get_new()
    if mod == 'hot':
        questions = models.Question.manager.get_hot()

    pages = len(questions) // PER_PAGE
    return render(request, template_name='index.html', context= { 'questions': paginate(questions, page= page, per_page= 5), 'pages': range(1, pages + 1), 'cur_page': str(page)})


def question(request):
    # pk = request.GET.get('answer_page', None)
    # if pk == None:
    #      return render(request, 'ask.html')


    question_id = int(request.GET.get('id'))
    question_item = QUESTIONS[question_id-1]
    page = request.GET.get('page', 1)
    pages = len(ANSWERS) // PER_PAGE
    print(QUESTIONS, QUESTIONS[1])
    return render(request, template_name='question.html', context= { 'question': question_item , 'answers': paginate(ANSWERS, page= page, per_page= 5),'pages': range(1, pages + 1)})


def registration(request):
    return render(request, template_name='registration.html')

def log_in(request):
    return render(request, template_name='login.html')

def auth(request):
    return render(request, template_name='auth-box.html')

def ask(request):
    return render(request, template_name='ask.html')

def settings(request):
    return render(request, template_name='settings.html')

def tag(request, tag):
    tag_instance = models.Tag.manager.get(name=tag)
    questions = tag_instance.questions.order_by('-likes_count', '-create_data', 'title')

    return render(request, template_name='tag.html', context= {'tag': tag_instance, 'questions': questions})