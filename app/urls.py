from django.urls import include, path
from app import views
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name = "hot"),
    path('question/<int:question_id>', views.question, name="question"),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('settings/', views.settings, name='settings'),
    path("signup/", views.signup, name="signup"),
    path("tag/<str:tag_name>", views.tag_page, name="tag_page"),
]