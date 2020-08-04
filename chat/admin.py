from django.contrib import admin
from chat import models

admin.site.register(models.GroupStatus)
admin.site.register(models.Group)
admin.site.register(models.ChatRoomStatus)
admin.site.register(models.ChatRoom)
admin.site.register(models.UserStatus)
admin.site.register(models.User)
admin.site.register(models.MemberStatus)
admin.site.register(models.Member)
admin.site.register(models.Message)
