import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth 
from django.contrib.auth.decorators import login_required
import app.utils 
from app import models
from app.forms import LoginForm, RegisterForm, QuestionForm, AnswerForm, SettingsForm
import copy
from django.views.decorators.http import require_POST

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

def index(request):
    questions = models.Question.objects.get_questions_with_counts()
    page = app.utils.paginate(questions, request, 5)
    popular_tags = models.Tag.objects.get_popular_tags()
    popular_members = models.Profile.objects.get_top_profiles()
    return render(
        request,
        'index.html',
        context={'questions': page.object_list, 'page_obj': page, 'popular_tags': popular_tags, 'popular_members': popular_members}
    )


def hot(request):
    questions = models.Question.objects.get_hot_questions()
    page = app.utils.paginate(questions, request, 5)
    popular_members = models.Profile.objects.get_top_profiles()
    popular_tags = models.Tag.objects.get_popular_tags()
    return render(
        request,
        'hot.html',
        context={'questions': page.object_list, 'page_obj': page, 'popular_tags': popular_tags, 'popular_members': popular_members}
    )

def question(request, question_id):
    if request.method == "POST":
        return app.utils.create_answer(request, question_id)
    one_question, answers = models.Question.objects.get_question_with_answers(question_id)
    page = app.utils.paginate(answers, request, 5)
    popular_tags = models.Tag.objects.get_popular_tags()
    popular_members = models.Profile.objects.get_top_profiles()
    return render(
        request,
        'question.html',
        {'question': one_question, 'answers': page.object_list, 'page_obj': page, 
            'popular_tags': popular_tags, 'popular_members': popular_members, 'form': AnswerForm()}
    )

def tag_page(request, tag_name):
    manager = models.Question.objects
    tag_questions = app.utils.find_page_with_tag(manager.get_by_tag(tag_name.lower()), tag_name.lower())
    popular_tags = models.Tag.objects.get_popular_tags()
    popular_members = models.Profile.objects.get_top_profiles()
    if tag_questions == []:
        return render(
            request,
            "layouts/base.html"
        )
    
    page = app.utils.paginate(tag_questions, request, 5)
    return render(
        request,
        "tag.html",
        {'questions': page.object_list, 'page_obj': page, 'tag_name': tag_name, 'popular_tags': popular_tags, 'popular_members': popular_members}
    )

@login_required
def ask(request):
    popular_tags = models.Tag.objects.get_popular_tags()
    popular_members = models.Profile.objects.get_top_profiles()

    if request.method == "POST":
        return app.utils.create_question(request, popular_tags, popular_members)

    return render(
        request, 
        'ask.html',
        {'popular_tags': popular_tags, 'popular_members': popular_members, 'form': QuestionForm()}
    )

def login(request):
    popular_tags = models.Tag.objects.get_popular_tags()
    popular_members = models.Profile.objects.get_top_profiles()
        
    if request.method == "POST":
        return app.utils.my_authenticate(request, popular_tags, popular_members)

    return render(
        request,
        "login.html",
        {'popular_tags': popular_tags, 'popular_members': popular_members, 'form' : LoginForm()}
    )

@login_required
def settings(request):
    popular_tags = models.Tag.objects.get_popular_tags()
    popular_members = models.Profile.objects.get_top_profiles()
    profile = models.Profile.objects.get(user__username=request.user)
    form = SettingsForm(instance=profile, user=request.user)
    if request.method == "POST":
        return app.utils.change_settings(request, popular_tags, popular_members)
    return render(
        request,
        "settings.html",
        {'popular_tags': popular_tags, 'popular_members': popular_members, 'form': form}
    )

def signup(request):
    popular_tags = models.Tag.objects.get_popular_tags()
    popular_members = models.Profile.objects.get_top_profiles()

    if request.method == "POST":
        return app.utils.create_profile(request, popular_tags, popular_members)
    return render(
        request,
        "signup.html",
        {'popular_tags': popular_tags, 'popular_members': popular_members, 'form': RegisterForm()}
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


    
