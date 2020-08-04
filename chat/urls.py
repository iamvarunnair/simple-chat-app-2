# chat/urls.py
from django.urls import path
from . import views
from django.conf.urls import url
from django.views.generic import RedirectView

urlpatterns = [
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('<str:room_name>/', views.room, name='room'),
    path('logout', views.logout, name='logout'),
    url(r'^$', RedirectView.as_view(pattern_name="login")),
]
