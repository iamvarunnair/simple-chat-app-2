# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('<str:room_name>/', views.room, name='room'),
    path('logout', views.logout, name='logout'),
]
