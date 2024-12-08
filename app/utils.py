from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from app import models
from django.contrib import auth
from django.contrib import messages
from app.forms import LoginForm, RegisterForm, QuestionForm, AnswerForm, SettingsForm


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
                print(tag_name)
                print(tag.tag_name.lower())
                tag_questions.append(question)

    if len(tag_questions) == 0:
        return []
    else:
        return tag_questions


def my_authenticate(request, popular_tags, popular_members):
    form = LoginForm(request.POST)
    if not form.is_valid():
        print(form.errors)
        return render(
            request,
            "login.html",
            {
                'form': form,
                'popular_tags': popular_tags,
                'popular_members': popular_members
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
                'popular_tags': popular_tags,
                'popular_members': popular_members,
            }
        )
    else:
        auth.login(request, user)
        return redirect("index")


def create_profile(request, popular_tags, popular_members):
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
                'popular_tags': popular_tags,
                'popular_members': popular_members,
            }
        )


def create_question(request, popular_tags, popular_members):
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
            'popular_tags': popular_tags,
            'popular_members': popular_members,
        }
    )

def create_answer(request, question_id):
    profile = models.Profile.objects.get(user__username=request.user)
    question = models.Question.objects.get(id = question_id)
    form = AnswerForm(request.POST)
    if form.is_valid():
        form.save(profile = profile, question = question)
        return redirect('question', question_id = question_id)
    return render(
        request,
        "question.html",
        {
            'form': form
        }
    )

def change_settings(request, popular_tags, popular_members):
    profile = models.Profile.objects.get(user__username=request.user)
    form = SettingsForm(request.POST, instance=profile, user=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Settings changed successfully')
    return render(
        request,
        "settings.html",
        {'popular_tags': popular_tags, 'popular_members': popular_members, 'form': form}
    )
    
