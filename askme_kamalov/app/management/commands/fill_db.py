from django.core.management.base import BaseCommand
from ...models import *
import requests
import lorem
from progress.bar import IncrementalBar
from random import randint
from random import sample


class Command(BaseCommand):
    help = 'Команда по заполнению БД данными'

    def add_arguments(self, parser):
        parser.add_argument(dest='ratio', type=int, default=True, action='store')

    def handle(self, *args, **options):
        ratio = options.get('ratio')
        tags = [Tag(name=f'{lorem.get_word()}{i}') for i in range(ratio)]
        Tag.manager.bulk_create(tags)
        del tags
        tags = Tag.manager.all()
        print("Tags created\n")

        names = [lorem.get_word() for i in range(ratio)]

        users = []
        bar = IncrementalBar('Users created', max=len(names))
        for name in names:
            users.append(User(username=f'{name}{len(users)}'))
            bar.next()
        bar.finish()
        User.objects.bulk_create(users)

        del users
        users = User.objects.all()
        print()

        questions = []
        bar = IncrementalBar('Questions created', max=len(users) * 10)
        for user in users:
            for i in range(10):
                title = f'question title{bar.index}'
                content = f'question content{bar.index}'
                question = Question(owner=user, title=title, text=content)
                questions.append(question)
                bar.next()
        bar.finish()
        Question.manager.bulk_create(questions)
        del questions
        questions = Question.manager.all()
        print()

        answers = []
        bar = IncrementalBar('Answers created', max=len(questions) * 100)
        for question in questions:
            for j in range(100):
                owner = users.exclude(id=question.owner.id).order_by('?').first()
                ans_content = f'answer content{bar.index}'
                answer = Answer(user_creator=owner, question=question, content=ans_content)
                answers.append(answer)
                bar.next()
        bar.finish()
        Answer.manager.bulk_create(answers)

        del answers
        answers = Answer.manager.get_queryset()
        print()

        bar = IncrementalBar('Tags added', max=len(questions))
        for question in questions:
            _tags = tags.order_by('?')[:randint(1, 6)]
            question.tags.set(_tags)
            bar.next()
        bar.finish()
        print()

        bar = IncrementalBar('Likes added', max=len(answers) * 200)
        for answer in answers:
            _users = users.order_by('?')[:10]
            likes = [Like(owner=owner, type='a') for owner in _users]
            likes = Like.manager.bulk_create(likes)
            answer.likes.set(likes)
            answer.likes_count = randint(1, 100)
            bar.next()
        bar.finish()
        Answer.manager.bulk_update(answers, ['likes_count'])