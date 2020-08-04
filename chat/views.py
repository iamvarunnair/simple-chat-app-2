from django.shortcuts import render, redirect
# Create your views here.
# chat/views.py
from django.utils.safestring import mark_safe
import json
from chat import models


def home(request):
    if request.session.has_key('user_id') & request.session.has_key('user_name'):
        return render(request, 'chat/home.html', {})
    return logout(request)


def room(request, room_name):
    if request.session.has_key('user_id') & request.session.has_key('user_name'):
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name))
        })
    return logout(request)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        output_json = {}
        if models.User.objects.filter(user_name__exact=username, status=1).exists():
            user_info_dict = models.User.objects.filter(
                user_name__exact=username).values().first()
            request.session['user_id'] = user_info_dict['user_id']
            request.session['user_name'] = user_info_dict['user_name']
            return redirect('home')
        else:
            return render(request, 'chat/login.html',
                          {'message': 'We don\'t know you, go away!', 'username': username})
    else:
        return render(request, 'chat/login.html', {})


def logout(request):
    if request.session.has_key('user_id'):
        del request.session['user_id']
    if request.session.has_key('user_name'):
        del request.session['user_name']
    return redirect('login')
