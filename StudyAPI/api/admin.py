from django.contrib import admin
from .models import Assignment, Subject, Subject_Info_Type, Chat, ChatMembership, Message

admin.site.register(Assignment)
admin.site.register(Subject)
admin.site.register(Subject_Info_Type)
admin.site.register(Chat)
admin.site.register(ChatMembership)
admin.site.register(Message)

