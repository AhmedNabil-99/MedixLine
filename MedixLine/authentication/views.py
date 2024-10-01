from django.shortcuts import render
from authentication.models import User
from authentication.serializers import UserSerializer
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages
from patients.serializers import PatientSerializer
from doctors.serializers import DoctorSerializer, SpecializationSerializer
from patients.models import Patient
from doctors.models import Doctor, Specialization
from rest_framework.generics import RetrieveUpdateAPIView


# Create your views here.

class UserDetailView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if created:
                token.delete()  # Delete the token if it was already created
                token = Token.objects.create(user=user)
            if user.role == 'patient':
                try:
                    patient = Patient.objects.get(user=user)
                except Patient.DoesNotExist:
                    return Response({'message': 'Patient profile not found'}, status=status.HTTP_404_NOT_FOUND)

                return Response({
                    'token': token.key,
                    'user': PatientSerializer(patient).data  
                })
            elif user.role == 'doctor':
                try:
                    doctor = Doctor.objects.get(user=user)
                except Doctor.DoesNotExist:
                    return Response({'message': 'Doctor profile not found'}, status=status.HTTP_404_NOT_FOUND)

                return Response({
                    'token': token.key,
                    'user': DoctorSerializer(doctor).data
                })

        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)



class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.headers) 
        token_key = request.auth.key
        token = Token.objects.get(key=token_key)
        token.delete()

        return Response({'detail': 'Successfully logged out.'})