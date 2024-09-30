from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Doctor, Specialization
from .serializers import DoctorSerializer, SpecializationSerializer, DoctorSerializerSet
from authentication.models import User


# Create your views here.

def send_activation_email(user, request):
    subject = "Medix Account Activation"
    uid = urlsafe_base64_encode(force_bytes(user.user.pk)) 
    print("uid",uid)
    activation_link = request.build_absolute_uri(reverse('activate-doctor', kwargs={'uidb64': uid}))
    message = f"Hello {user.user.first_name}, please click the link to activate your account: {activation_link}"

    send_mail(
        subject,
        message,
        'MedixLine <an63805@gmail.com>',  
        [user.user.email], 
        fail_silently=False,
    )


    
def activate(request, uidb64):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid) 
        user.is_active = True 
        user.save()
        messages.success(request, 'Account activated successfully! You can now log in.')
        return redirect('http://localhost:3000/signin') 
    except User.DoesNotExist:
        print(request)
        messages.error(request, 'Invalid activation link')
        return redirect('http://localhost:3000/signup')


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializerSet

class DoctorRegistrationView(APIView):
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            send_activation_email(user, request)
            messages.success(request, f'Dear {user.user.first_name}, please go to your email inbox and click on the received activation link to confirm and complete the registration. Check your spam folder if necessary.')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all() 
    serializer_class = SpecializationSerializer