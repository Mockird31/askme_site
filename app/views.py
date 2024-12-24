import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth 
from django.contrib.auth.decorators import login_required
import app.utils 
from app import models
from app.forms import LoginForm, RegisterForm, QuestionForm, AnswerForm, SettingsForm
import copy
from django.views.decorators.http import require_POST, require_GET
import functools
import operator
from django.db.models import Q

QUESTIONS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'This is text for question № {i}',
        'tags': ['it', 'engineering', 'chemistry', "math"],
        'num_answers': i,
        'answers': [f'This is an answer {j} for question' for j in range(5)]
    } for i in range(30)
]

# Create your views here.
@require_GET
def search(request):
    query = request.GET.get('q')
    if not query:
        return redirect('index')
    queries = query.split()
    query_set = functools.reduce(operator.__or__, [Q(search_vector__icontains=query) for query in queries])
    matched_questions = models.Question.objects.filter(query_set).distinct()
    print(matched_questions)
    page = app.utils.paginate(matched_questions, request, 5)

    return render(
        request,
        'search_result.html',
        context={'questions': page.object_list, 'page_obj': page}
    )


def index(request):
    questions = models.Question.objects.get_questions_with_counts()
    page = app.utils.paginate(questions, request, 5)
    return render(
        request,
        'index.html',
        context={'questions': page.object_list, 'page_obj': page}
    )

def hot(request):
    questions = models.Question.objects.get_hot_questions()
    page = app.utils.paginate(questions, request, 5)
    return render(
        request,
        'hot.html',
        context={'questions': page.object_list, 'page_obj': page}
    )

def question(request, question_id):
    if request.method == "POST":
        return app.utils.create_answer(request, question_id)
    one_question, answers = models.Question.objects.get_question_with_answers(question_id)
    page = app.utils.paginate(answers, request, 5)
    return render(
        request,
        'question.html',
        {'question': one_question, 'answers': page.object_list, 'page_obj': page, 'form': AnswerForm()}
    )

def tag_page(request, tag_name):
    manager = models.Question.objects
    tag_questions = app.utils.find_page_with_tag(manager.get_by_tag(tag_name.lower()), tag_name.lower())
    if tag_questions == []:
        return render(
            request,
            "layouts/base.html"
        )
    
    page = app.utils.paginate(tag_questions, request, 5)
    return render(
        request,
        "tag.html",
        {'questions': page.object_list, 'page_obj': page, 'tag_name': tag_name}
    )

@login_required
def ask(request):
    if request.method == "POST":
        return app.utils.create_question(request)

    return render(
        request, 
        'ask.html',
        {'form': QuestionForm()}
    )

def login(request):
        
    if request.method == "POST":
        return app.utils.my_authenticate(request)

    return render(
        request,
        "login.html",
        {'form' : LoginForm()}
    )

@login_required
def settings(request):
    profile = models.Profile.objects.get(user__username=request.user)
    form = SettingsForm(instance=profile, user=request.user)
    if request.method == "POST":
        return app.utils.change_settings(request)
    return render(
        request,
        "settings.html",
        {'form': form}
    )

def signup(request):
    if request.method == "POST":
        return app.utils.create_profile(request)
    return render(
        request,
        "signup.html",
        {'form': RegisterForm()}
    )

def logout(request):
    auth.logout(request)
    return redirect('index')

@require_POST 
@login_required
def like_question_async(request, question_id):
    data = app.utils.get_like_async_info_question(request, question_id)
    return JsonResponse(data)

@require_POST 
@login_required
def dislike_question_async(request, question_id):
    data = app.utils.get_dislike_async_info_question(request, question_id)
    return JsonResponse(data)

@require_POST
@login_required
def pick_correct_answer(request, answer_id):
    data = app.utils.get_correct_answer_info(request, answer_id)
    return JsonResponse(data)  


@require_POST 
@login_required
def like_answer_async(request, answer_id):
    data = app.utils.get_like_async_info_answer(request, answer_id)
    return JsonResponse(data)

@require_POST 
@login_required
def dislike_answer_async(request, answer_id):
    data = app.utils.get_dislike_async_info_answer(request, answer_id)
    return JsonResponse(data)

def test_view(request):
    return render(
        request,
        "test.html"
    )