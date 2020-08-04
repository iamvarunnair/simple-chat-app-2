from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from chat import models, serializers
from django.shortcuts import render, redirect


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Step 1: fetch room name from url
    Step 2: check if group name exists for room name, if it does, goto step 4, else goto next step
    Step 3: create group in group table
    Step 4: check if chat room exists, if it does, goto step 6, else goto next step
    Step 5: create chat room in chat room table
    Step 6: check if member exists for chat room, if it does, goto step 8, else goto next step
    Step 7: create memeber for chat room
    Step 8: fetch last 50 messages for the chat room
    Step 9: send messages and accept connection.
    """
    async def connect(self):
        user_id = await self.get_key_in_session('user_id')
        user_name = await self.get_key_in_session('user_name')
        if user_id != None and user_name != None:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            user_details = await self.get_or_create_chat_room(
                self.room_name, user_id, user_name
            )
            self.user_details = user_details
            self.room_group_name = self.user_details['group']['name']
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            accept_response = await self.accept()
            print('history: ', self.user_details['message_history'])
            await self.send(text_data=json.dumps({
                'message': self.user_details['message_history']
            }))
        else:
            await self.close()

    """
    Step 1: discard group
    Step 2: change member status to inactive
    Step 3: check if member was the last member in the chat, change chat status and group status to inactive
    """
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.on_close_group(self.user_details['chat_room']['id'], self.user_details['group']['id'])

    """
    Step 1: add message to messages model
    Step 2: send it to everyone in the group
    """
    # Receive message from web socket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = self.user_details['user']['name'] + \
            ': ' + text_data_json['message']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        await self.add_message_to_db(message, self.user_details['chat_room']['id'], self.user_details['member']['id'])

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': [message]
        }))

    @database_sync_to_async
    def get_or_create_chat_room(self, room_name, user_id, user_name):
        output_json = {}
        group_name_exists_bool = models.Group.objects.filter(
            group_name__exact='group_'+room_name).exists()

        if group_name_exists_bool == False:
            group_dict = {
                'group_name': 'group_' + room_name,
                'status': 1,
                'created_by': 'Varun'
            }
            group_serializer = serializers.GroupSerializer(data=group_dict)
            if group_serializer.is_valid(raise_exception=True):
                fetched_group = group_serializer.save()
                fetched_group = dict(fetched_group.__dict__)
        else:
            fetched_group = models.Group.objects.filter(
                group_name__exact='group_'+room_name).values().first()

        room_name_exists_bool = models.ChatRoom.objects.filter(
            chat_room_name__exact=room_name).exists()

        if room_name_exists_bool == False:
            chat_room_dict = {
                'chat_room_name': room_name,
                'group_id': fetched_group['group_id'],
                'port_number': 9876,
                'type_name': 'user_defined_group',
                'status': 1
            }
            chat_room_serializer = serializers.ChatRoomSerializer(
                data=chat_room_dict)
            if chat_room_serializer.is_valid(raise_exception=True):
                fetched_chat_room = chat_room_serializer.save()
                fetched_chat_room = dict(fetched_chat_room.__dict__)
        else:
            fetched_chat_room = models.ChatRoom.objects.filter(
                chat_room_name__exact=room_name, group_id=fetched_group['group_id']).values().first()

        member_exists_bool = models.Member.objects.filter(
            chat_room_id=fetched_chat_room['chat_room_id'], user_id=user_id).exists()
        if member_exists_bool == False:
            member_dict = {
                'user_id': user_id,
                'chat_room_id': fetched_chat_room['chat_room_id'],
                'status': 1
            }
            member_serializer = serializers.MemberSerializer(
                data=member_dict)
            if member_serializer.is_valid(raise_exception=True):
                fetched_member = member_serializer.save()
                fetched_member = dict(fetched_member.__dict__)
        else:
            fetched_member = models.Member.objects.filter(
                chat_room_id=fetched_chat_room['chat_room_id'], user_id=user_id).values().first()

        fetched_messages = models.Message.objects.filter(
            chat_room_id__exact=fetched_chat_room['chat_room_id']).values_list('message_body', flat=True)[:50]

        output_json = {
            'chat_room': {
                'id': fetched_chat_room['chat_room_id'],
                'name': fetched_chat_room['chat_room_name']
            },
            'group': {
                'id': fetched_group['group_id'],
                'name': fetched_group['group_name']
            },
            'member': {
                'id': fetched_member['member_id']
            },
            'user': {
                'id': user_id,
                'name': user_name
            },
            'message_history': list(fetched_messages)
        }
        return output_json

    @database_sync_to_async
    def add_message_to_db(self, message_body, chat_room_id, member_id):
        message_dict = {
            'message_body': message_body,
            'chat_room_id': chat_room_id,
            'member_id': member_id
        }
        message_serializer = serializers.MessageSerializer(
            data=message_dict)
        if message_serializer.is_valid(raise_exception=True):
            message_serializer.save()

    @database_sync_to_async
    def on_close_group(self, chat_room_id, group_id):
        models.Group.objects.filter(
            group_id__exact=group_id).update(status=2)
        models.ChatRoom.objects.filter(
            chat_room_id__exact=chat_room_id).update(status=2)
    """
    For some reason self.scope['session'] stopped working (had problem accessing db from async cycle)
    in async consumers even though SessionMiddlewareStack was implemented
    in channel_tut.routing thus had to create a sync_to_async function.
    """
    @sync_to_async
    def get_key_in_session(self, key):
        if self.scope['session'].has_key(key):
            return self.scope['session'].get(key)
        return None
