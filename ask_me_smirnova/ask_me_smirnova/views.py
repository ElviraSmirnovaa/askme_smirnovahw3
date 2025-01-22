import copy
from lib2to3.fixes.fix_input import context
from pydoc import pager
from tkinter.messagebox import QUESTION

from django.contrib.admin.templatetags.admin_list import pagination
from django.core.paginator import Paginator, InvalidPage
from django.http import HttpResponse, Http404
from django.shortcuts import render
from app.models import Tag, Question, QuestionLike, Answer, AnswerLike
from django.contrib.auth.models import User
from django.db.models import Count

def pagination(objects_list, request, per_page=10):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(objects_list, per_page)
    try:
        page = paginator.page(page_num)
    except InvalidPage:
        raise Http404("Страница не найдена")
    return page


def index(request):
    questions = Question.objects.get_newest()
    page = pagination(questions, request)
    return render(
        request, 'index.html',
        context={'questions': page.object_list, 'page_obj': page})


def question(request, question_id):
    question = Question.objects.prefetch_related('tags').get(id=question_id)
    likes = QuestionLike.objects.filter(question=question).count()
    print(likes)
    answers = Answer.objects.annotate(num_likes=Count('a_likes')).filter(question_id=question_id)
    page = pagination(answers, request, 5)
    return render(request, 'question.html', context={'question': question, 'answers': page.object_list, 'page_obj': page, 'q_likes': likes})


def hot(request):
    questions = Question.objects.get_hot()
    page = pagination(questions, request)
    return render(
        request, 'hot.html',
        context={'questions': page.object_list, 'page_obj': page})


def tag(request, tag_name):
    questions = Question.objects.get_by_tag(tag_name)
    page = pagination(questions, request, 5)
    return render(request, 'tag.html', context={'questions': page.object_list, 'tag_name': tag_name, 'page_obj': page})


def settings(request):
    return render(request, 'setting.html')


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')
