from cent import Client, PublishRequest
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from app import models
from django.contrib import auth
from django.contrib import messages
from app.forms import LoginForm, RegisterForm, QuestionForm, AnswerForm, SettingsForm
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.db.models import Count
from askme_inyakin import settings

def paginate(object_list, request, per_page=10):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(object_list, per_page)
    try:
        page_num = int(page_num)
    except ValueError:
        page_num = paginator.num_pages
    page = paginator.get_page(page_num)
    return page


def find_page_with_tag(QUESTIONS, tag_name):
    tag_questions = []
    for question in QUESTIONS:
        for tag in question.tags.all():
            if tag_name.lower() == tag.tag_name.lower():
                tag_questions.append(question)

    if len(tag_questions) == 0:
        return []
    else:
        return tag_questions


def my_authenticate(request):
    form = LoginForm(request.POST)
    if not form.is_valid():
        return render(
            request,
            "login.html",
            {
                'form': form,
            }
        )
    
    user = auth.authenticate(request, **form.cleaned_data)

    if user is None:
        form.add_error(None, "Wrong username or password")
        return render(
            request,
            "login.html",
            {
                'form': form,
            }
        )
    else:
        auth.login(request, user)
        return redirect("index")


def create_profile(request):
    form = RegisterForm(request.POST, request.FILES)
    if form.is_valid():
        profile = form.save()
        auth.login(request, profile.user)
        return redirect('index')
    return render(
            request,
            "signup.html",
            {
                'form': form,
            }
        )


def create_question(request):
    if (not models.Profile.objects.filter(user__username=request.user).exists()):
        messages.error(request, 'This profile does not exist')
        return render(
            request,
            "ask.html",
            {
                'form': QuestionForm(),
            }
        )
    profile = models.Profile.objects.get(user__username=request.user)
    form = QuestionForm(request.POST)
    if form.is_valid():
        question = form.save(profile=profile)
        return redirect('question', question_id = question.id)
    return render(
        request,
        "ask.html",
        {
            'form': form,
        }
    )

def create_answer(request, question_id):
    profile = models.Profile.objects.get(user__username=request.user)
    question = models.Question.objects.get(id = question_id)
    form = AnswerForm(request.POST)
    if form.is_valid():
        answer = form.save(profile = profile, question = question)
        answer.profile = profile
        answer.question = question
        answer = models.Answer.objects.annotate(
            like_count=Count('answerlike'),
            dislike_count=Count('answerdislike')
        ).get(id=answer.id)

        client = Client(settings.CENTRIFUGO_API_URL, settings.CENTRIFUGO_API_KEY)
        request_cent = PublishRequest(channel=str(question.id), data={
            "answer_id": answer.id,
            "user_id": answer.profile.user.id,
            "image_path": answer.profile.get_avatar_url(),
            "username": answer.profile.user.username,
            "text": answer.text,
        })
        print(profile.get_avatar_url())
        result = client.publish(request_cent)
        return redirect('question', question_id = question_id)
    return render(
        request,
        "question.html",
        {
            'form': form
        }
    )

def change_settings(request):
    profile = models.Profile.objects.get(user__username=request.user)
    form = SettingsForm(request.POST, request.FILES, instance=profile, user=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Settings changed successfully')
    return render(
        request,
        "settings.html",
        {'form': form}
    )
    
def check_is_liked_question(question: models.Question, user: models.User):
    has_liked = False
    if user.is_authenticated:
        profile = models.Profile.objects.get(user=user)
        has_liked = models.QuestionLike.objects.filter(question=question, profile=profile).exists()
    return has_liked

def check_is_disliked_question(question: models.Question, user: models.User):
    has_disliked = False
    if user.is_authenticated:
        profile = models.Profile.objects.get(user=user)
        has_disliked = models.QuestionDislike.objects.filter(question=question, profile=profile).exists()
    return has_disliked

def get_like_async_info_question(request, question_id: int) -> dict:
    profile = models.Profile.objects.get(user=request.user)
    question = models.Question.objects.get(id=question_id)

    models.QuestionDislike.objects.filter(question=question, profile=profile).delete()

    like, created = models.QuestionLike.objects.get_or_create(question=question, profile=profile)
    if not created:
        like.delete()

    likes_count = models.QuestionLike.objects.filter(question=question).count()
    dislikes_count = models.QuestionDislike.objects.filter(question=question).count()

    return {
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
    }

def get_dislike_async_info_question(request, question_id: int) -> dict:
    profile = models.Profile.objects.get(user=request.user)
    question = models.Question.objects.get(id=question_id)

    models.QuestionLike.objects.filter(question=question, profile=profile).delete()

    dislike, created = models.QuestionDislike.objects.get_or_create(question=question, profile=profile)
    if not created:
        dislike.delete()

    likes_count = models.QuestionLike.objects.filter(question=question).count()
    dislikes_count = models.QuestionDislike.objects.filter(question=question).count()

    return {
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
    }

def get_correct_answer_info(request, answer_id):
    profile = models.Profile.objects.get(user=request.user)
    answer = models.Answer.objects.get(id=answer_id)
    question = answer.question
    if (profile != question.profile):
        return {'status': 'error', 'message': 'You are not allowed to pick correct answer for this question'}
    if (answer.is_correct == 'c'):
        answer.is_correct = 'p'
    else:
        answer.is_correct = 'c' 
    answer.save()  
    return {'status': 'ok', 'is_correct': answer.is_correct}



def get_like_async_info_answer(request, answer_id: int) -> dict:
    profile = models.Profile.objects.get(user=request.user)
    answer = models.Answer.objects.get(id=answer_id)
    models.AnswerDislike.objects.filter(answer=answer, profile=profile).delete()

    like, created = models.AnswerLike.objects.get_or_create(answer=answer, profile=profile)
    if not created:
        like.delete()

    likes_count = models.AnswerLike.objects.filter(answer=answer).count()
    dislikes_count = models.AnswerDislike.objects.filter(answer=answer).count()

    return {
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
    }

def get_dislike_async_info_answer(request, answer_id: int) -> dict:
    profile = models.Profile.objects.get(user=request.user)
    answer = models.Answer.objects.get(id=answer_id)
    models.AnswerLike.objects.filter(answer=answer, profile=profile).delete()

    dislike, created = models.AnswerDislike.objects.get_or_create(answer=answer, profile=profile)
    if not created:
        dislike.delete()

    likes_count = models.AnswerLike.objects.filter(answer=answer).count()
    dislikes_count = models.AnswerDislike.objects.filter(answer=answer).count()

    return {
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
    }