from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import PatientSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from .models import Patient
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import render, redirect 
from django.urls import reverse
from authentication.models import User
from rest_framework.permissions import IsAuthenticated






def send_activation_email(user, request):
    subject = "Medix Account Activation"
    uid = urlsafe_base64_encode(force_bytes(user.user.pk)) 
    print("act_mail",uid)
    activation_link = request.build_absolute_uri(reverse('activate-patient', kwargs={'uidb64': uid}))
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
        messages.error(request, 'Invalid activation link')
        return redirect('http://localhost:3000/signup')



class PatientViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]


class PatientRegistrationView(APIView):
    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            send_activation_email(user, request)
            messages.success(request, f'Dear {user.user.first_name}, please go to your email inbox and click on the received activation link to confirm and complete the registration. Check your spam folder if necessary.')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Login view
# class UserLoginView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             token, created = Token.objects.get_or_create(user=user)
#             if created:
                # token.delete()                                              # Delete the token if it was already created
                # token = Token.objects.create(user=user)

            # response_data = {
            #     'token': token.key,
            #     'username': user.username,
            #     'role': user.role,
            # }

            # if user.role == 'patient':
            #     patient = user.patient_account                                 # Assuming the related name is "student_account"
                # if patient is not None:
                                                                                         # Add student data to the response data
        #             patient_data = PatientSerializer(patient).data
        #             response_data['data'] = patient_data

        #     return Response(response_data)
        # else:
        #     return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)