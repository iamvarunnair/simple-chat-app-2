from datetime import datetime
from django.db import models


class GroupStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(
        max_length=100, default=None)  # inactive,active

    def __str__(self):
        return str(self.status_id)


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=60)
    status = models.ForeignKey(
        GroupStatus, on_delete=models.CASCADE, default=None)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.CharField(max_length=100, default=None)

    def __str__(self):
        return str(self.group_id)


class ChatRoomStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(
        max_length=100, default=None)  # inactive,active

    def __str__(self):
        return str(self.status_id)


class ChatRoom(models.Model):
    chat_room_id = models.AutoField(primary_key=True)
    chat_room_name = models.CharField(max_length=100)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, default=None)
    port_number = models.PositiveSmallIntegerField(
        default=1, blank=True, null=True)  # 8000,9000,7000
    # 1-1,open_group,user_define_group
    type_name = models.CharField(max_length=100, default=None)
    status = models.ForeignKey(
        ChatRoomStatus, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.chat_room_id)


class UserStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(
        max_length=100, default=None)  # active,inactive

    def __str__(self):
        return str(self.status_id)


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=60, unique=True)
    status = models.ForeignKey(
        UserStatus, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.user_id)


class MemberStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(
        max_length=100, default=None)  # active,inactive

    def __str__(self):
        return str(self.status_id)


class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None)
    chat_room_id = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, default=None)
    status = models.ForeignKey(
        MemberStatus, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.member_id)


class Message(models.Model):

    message_id = models.AutoField(primary_key=True)
    message_body = models.TextField(max_length=400, default=None)
    message_time = models.DateTimeField(auto_now_add=True, blank=True)
    chat_room_id = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, default=None)
    member_id = models.ForeignKey(
        Member, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.message_id)
