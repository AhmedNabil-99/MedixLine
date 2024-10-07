from django.shortcuts import render
from .serializers import chatserializer
from chats.models import Chat
from authentication.models import User
from rest_framework import generics
from django.db.models import Subquery , OuterRef , Q
from authentication.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class MyInbox(generics.ListAPIView):
    serializer_class = UserSerializer  # Use UserSerializer to return user details
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the logged-in doctor (authenticated user)
        doctor = self.request.user

        # Filter patients who have sent or received messages from the doctor
        patients = User.objects.filter(
            Q(sender__reciever=doctor) |  # Patients who sent messages to the doctor
            Q(reciever__sender=doctor)    # Patients who received messages from the doctor
        ).distinct()

        return patients


class GetMessages(generics.ListAPIView):
    serializer_class = chatserializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        reciever_id = self.kwargs['reciever_id']

        messages = Chat.objects.filter(
          sender__in=[sender_id, reciever_id],
          reciever__in=[sender_id, reciever_id]
        )  

        return messages
    
class SendMessage(generics.CreateAPIView):
    serializer_class = chatserializer


class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class SearchUser(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        loged_on_user = self.request.user
        users = User.objects.filter(
             Q(username__icontains=username) |
             Q(first_name__icontains=username) |
             Q(last_name__icontains=username) |
             Q(email__icontains=username)
        )
        if not users.exists():
            return Response({"detail": "No user found."}, 
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)