from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.logins, name='login'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.logout_me, name='logout_me'),
    path('like/', views.like_vote, name='like_vote'),
    path('dislike/', views.dislike_vote, name='dislike_vote'),
    path('delete/', views.delete, name='delete'),
    path('upgrate/', views.upgrate, name='upgrate'),
]