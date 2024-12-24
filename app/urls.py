from django.urls import include, path
from app import views
from django.contrib import admin
from askme_inyakin import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name = "hot"),
    path('question/<int:question_id>', views.question, name="question"),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('settings/', views.settings, name='settings'),
    path("signup/", views.signup, name="signup"),
    path("tag/<str:tag_name>", views.tag_page, name="tag_page"),
    path('logout/', views.logout, name='logout'),
    path("<int:question_id>/like_question_async", views.like_question_async, name='like_question_async'),
    path("question/<int:question_id>/like_question_async", views.like_question_async, name='like_question_async'),
    path("<int:question_id>/dislike_question_async", views.dislike_question_async, name='dislike_question_async'),
    path("question/<int:question_id>/dislike_question_async", views.dislike_question_async, name='dislike_question_async'),
    path("<int:answer_id>/pick_correct_answer", views.pick_correct_answer, name='pick_correct_answer'),
    path("<int:answer_id>/like_answer_async", views.like_answer_async, name='like_answer_async'),
    path("<int:answer_id>/dislike_answer_async", views.dislike_answer_async, name='dislike_answer_async'),
    path("search", views.search, name='search'),
]

if settings.DEBUG:
    urlpatterns += [path("test/", views.test_view, name='test_view')]
