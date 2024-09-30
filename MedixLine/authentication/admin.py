from django.contrib import admin
from chats.models import Chat
# Register your models here.


class ChatAdmin(admin.ModelAdmin):
    list_display = ['is_read']
    list_filter = ['sender', 'reciever', 'message' ,'is_read']


admin.site.register(Chat , ChatAdmin)