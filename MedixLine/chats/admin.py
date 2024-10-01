from django.contrib import admin
from chats.models import Chat


class ChatAdmin(admin.ModelAdmin):
    list_editable = ('is_read',)
    list_display = ('sender' , 'reciever' , 'message' , 'is_read' , 'date')


admin.site.register(Chat, ChatAdmin)