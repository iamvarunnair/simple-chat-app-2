from django.shortcuts import render
# Create your views here.
# chat/views.py
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from chat.models import Group, User
from django.core.serializers.json import DjangoJSONEncoder
from chat.serializers import UserSerializer, UserToChatRoomMappingSerializer
import json
from django.http import JsonResponse
import pdb


def removemember(request):

    if request.session.has_key('user_id') & request.session.has_key('user_name'):
       return render(request, 'chat/home.html', {})
    return logout(request)


def remove_member(request):
    if request.session.has_key('user_id') & request.session.has_key('user_name'):
        import pdb
        pdb.set_trace()
        input_json = request
        removemember = []
        output_json = {}
        remove_member_details = {}
        selected_users = json.loads(request.body)['selected_users']
        group_details = json.loads(request.body)[
            'group_details']['group_id']
        try:
            member_exists_bool = UserToChatRoomMapping.objects.filter(group_id=group_details, user_id__in=selected_users,status=1).exists()
            
            if member_exists_bool == False:
                for i in selected_users:
                    remove_member_details = {}
                    remove_member_details['user_id'] = i
                    remove_member_details['group_id'] = group_details
                    remove_member_details['status'] = 2
                    removemember.append(remove_member_details)
                    member_serializer = UserToChatRoomMappingSerializer(
                        data=remove_member_details, many=True)
                    if member_serializer.is_valid(raise_exception=True):
                        member_serializer.save()
                        fetched_member = UserToChatRoomMapping.objects.filter(group_id=fetched_group['group_id']).values('user_id')
                        remaining_users=User.objects.exclude(user_id__in=fetched_member)
                        output_json['status'] = "Success"
                        output_json['message'] = "removing members successfully in group"
                        
                        return JsonResponse(output_json)
                    else:
                        fetched_member = UserToChatRoomMapping.objects.filter(group_id=fetched_group['group_id']).values('user_id')
                        remaining_users=User.objects.exclude(user_id__in=fetched_member)
                        output_json['status'] = "Success"
                        output_json['message'] = "removing members successfully in group"
                        return JsonResponse(output_json)
                    
        except Exception as ex:
            output_json['Status'] = 'Failure'
            output_json['Message'] = 'Error occured while removing member details.' + \
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
