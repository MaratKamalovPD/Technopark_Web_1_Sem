from django.shortcuts import render
from django.core.paginator import Paginator
QUESTIONS = [
        {
            'id': i,
            'title': f'Question {i}',
            'text': f'Text {i}'
        } for i in range(20)
    ]
def paginate(objects, page, per_page=4):
    paginator = Paginator(objects, per_page)
    page_items = paginator.page(1).object_list
    return paginator.page(page)

# Create your views here.
def index(request):
    page = request.GET.get('page', 1)
    return render(request, template_name='index.html', context= { 'questions': paginate(QUESTIONS, page= page, per_page= 5)})

def question(request, question_id):
    question_item = QUESTIONS[question_id]
    return render(request, template_name='question.html', context= { 'question': question_item})