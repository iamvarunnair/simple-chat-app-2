from django.shortcuts import render
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import datetime
from chat.models import Message
from django.core.serializers.json import DjangoJSONEncoder
from chat.serializers import UserSerializer, UserToChatRoomMappingSerializer
from django.http import HttpResponse


def delete_message(request):

    if request.session.has_key('user_id') & request.session.has_key('user_name'):
       return render(request, 'chat/home.html', {})
    return logout(request)

    
def delete_message_before_one_hour(request):
    if request.session.has_key('user_id') & request.session.has_key('user_name'): 
        import pdb;pdb.set_trace()
        output_json ={}
        input_json =request
        try:
            fetched_messages = Message.objects.filter(group_id__exact=input_json['group_id'])
            message_time = fetched_messages.message_send_date
            year_count_var =abs(datetime.now().year - int(message_time[0][0:4]))
            months_count_var =abs(datetime.now().month - int(message_time[0][5:7]))
            days_count_var =abs(datetime.now().day - int(message_time[0][8:10]))
            hours_count_var = abs(datetime.now().hour- int(message_time[0][11:15]))
            delete_message ={}
            if year_count_var <=0:
                if months_count_var <=0:
                    if days_count_var <=0:
                        if hours_count_var <=0:
                            delete_flag =1
                            if delete_flag==1:
                                delete_message['message_status'] =2
                                delete_message['group_id'] =input_json['group_id']
                                message_serializer=MessageSerializer(data=delete_message,partial=True)
                                if message_serializer.is_valid(raise_excepton):
                                    message_serializer.save()
                                    delete_message_for_everyone =Message.objects.filter(group_id__exact=fetched_group['group_id']).update(message_status =2)
                                    output_json['Status'] ="Success"
                                    output_json['Message'] ="Delete message for everyone"
                                    return output_json
                            else:
                                delete_message['message_status'] =3
                                delete_message['member_id'] =input_json['member_id']
                                message_serializer=MessageSerializer(data=delete_message,partial=True)
                                if message_serializer.is_valid(raise_excepton):
                                    message_serializer.save()
                                    delete_message_for_me =Message.objects.filter(group_id__exact=fetched_group['group_id']).update(message_status =2)
                                    output_json['Status'] ="Success"
                                    output_json['Message'] ="Delete message for Me"
                                    return output_json
            return output_json
        except Exception as ex:
            output_json['Status'] ="Failure"
            output_json['Message'] ="Some internal issue while delete message before one hour"
            return output_json
