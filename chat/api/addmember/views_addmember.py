from django.shortcuts import render
# Create your views here.
# chat/views.py
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from rest_framework.response import Response
from django.http import JsonResponse
from chat.models import Group, User, UserToChatRoomMapping
from django.core.serializers.json import DjangoJSONEncoder
from chat.serializers import UserSerializer, UserToChatRoomMappingSerializer
import json
import pdb
from django.http import HttpResponse


def member(request):

    if request.session.has_key('user_id') & request.session.has_key('user_name'):
       return render(request, 'chat/home.html', {})
    return logout(request)


def add_member(request):
    import pdb
    pdb.set_trace()
    if request.session.has_key('user_id') & request.session.has_key('user_name'):        
        input_json = request
        addmember = []
        output_json = {}
        add_member_details = {}
        selected_users = json.loads(request.body)['selected_users']
        group_details = json.loads(request.body)[
            'group_details']['group_id']
        try:
            member_exists_bool = UserToChatRoomMapping.objects.filter(
                group_id=group_details, user_id__in=selected_users,status=1).exists()
            if member_exists_bool == False:
                for i in selected_users:
                    add_member_details = {}
                    add_member_details['user_id'] = i
                    add_member_details['group_id'] = group_details
                    add_member_details['status'] = 1
                    addmember.append(add_member_details)
                member_serializer = UserToChatRoomMappingSerializer(
                    data=addmember, many=True)
                if member_serializer.is_valid(raise_exception=True):
                   member_serializer.save()
                   member_details=(list(UserToChatRoomMapping.objects.filter(group_id=group_details,user_id__in=selected_users).values('user_id')))
                   output_json['status'] = "Success"
                   output_json['message'] = "adding members successfully in group"
                   output_json['adding_member_list']=member_details
                   
                   return JsonResponse(output_json,safe=False)
            else:
                fetched_member = (list(UserToChatRoomMapping.objects.filter(
                    group_id=group_details, user_id__in=selected_users,status=1).values('user_id')))
            
                output_json['status'] = "Success"
                output_json['message'] = "adding members successfully in group"
                output_json['adding_member_list']=fetched_member
                return JsonResponse(output_json,safe=False)
        except Exception as ex:
            output_json['Status'] = 'Failure'
            output_json['Message'] = 'Error occured while fetching member details.' + \
                str(ex)
            return JsonResponse(output_json, 'chat/group.html')

    return logout(request)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        output_json = {}
        if User.objects.filter(user_name__exact=username, status=1).exists():
            user_info_dict = User.objects.filter(
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
