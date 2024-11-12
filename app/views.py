from django.http import HttpResponse
from django.shortcuts import render
import app.utils 
from app import models
import copy

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
    one_question, answers = models.Question.objects.get_question_with_answers(question_id)
    page = app.utils.paginate(answers, request, 5)
    popular_tags = models.Tag.objects.get_popular_tags()
    popular_members = models.Profile.objects.get_top_profiles()
    return render(
        request,
        'question.html',
        {'question': one_question, 'answers': page.object_list, 'page_obj': page, 'popular_tags': popular_tags, 'popular_members': popular_members}
    )

def tag_page(request, tag_name):
    manager = models.Question.objects
    tag_questions = app.utils.find_page_with_tag(manager.get_by_tag(tag_name.capitalize()), tag_name.capitalize())
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

def ask(request):
    popular_tags = models.Tag.objects.get_popular_tags()
    popular_members = models.Profile.objects.get_top_profiles()
    return render(
        request, 
        'ask.html',
        {'popular_tags': popular_tags, 'popular_members': popular_members}
    )

def login(request):
    popular_tags = models.Tag.objects.get_popular_tags()
    popular_members = models.Profile.objects.get_top_profiles()
    return render(
        request,
        "login.html",
        {'popular_tags': popular_tags, 'popular_members': popular_members}
    )

def settings(request):
    popular_tags = models.Tag.objects.get_popular_tags()
    popular_members = models.Profile.objects.get_top_profiles()
    return render(
        request,
        "settings.html",
        {'popular_tags': popular_tags, 'popular_members': popular_members}
    )

def signup(request):
    popular_tags = models.Tag.objects.get_popular_tags()
    popular_members = models.Profile.objects.get_top_profiles()
    return render(
        request,
        "signup.html",
        {'popular_tags': popular_tags, 'popular_members': popular_members}
    )