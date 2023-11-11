from django.shortcuts import render
from django.core.paginator import Paginator

PER_PAGE = 5
QUESTIONS = [
        {
            'id': i,
            'title': f'Question {i}',
            'text': f'Text {i}'
        } for i in range(40)
    ]
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
    pages = len(QUESTIONS) // PER_PAGE
    return render(request, template_name='index.html', context= { 'questions': paginate(QUESTIONS, page= page, per_page= 5), 'pages': range(1, pages + 1), 'cur_page': str(page) })


def question(request):
    # pk = request.GET.get('answer_page', None)
    # if pk == None:
    #      return render(request, 'ask.html')


    question_id = int(request.GET.get('id'))
    question_item = QUESTIONS[question_id]
    page = request.GET.get('page', 1)
    pages = len(ANSWERS) // PER_PAGE
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

def tag(request):
    return render(request, template_name='tag.html')