from chats.models import Chat 
from rest_framework import serializers
from authentication.serializers import UserSerializer

class chatserializer(serializers.ModelSerializer):
    reciever_profile = UserSerializer(read_only=True)
    sender_profile = UserSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = ['id','sender_profile','reciever_profile','sender', 'reciever', 'message', 'date' , 'is_read']