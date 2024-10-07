from django.shortcuts import render, redirect
from rest_framework import viewsets, status,permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
from .models import Doctor, Specialization,Rating,Comment
from .serializers import DoctorSerializer, SpecializationSerializer, DoctorSerializerSet,RatingSerializer,CommentSerializer
from .models import Doctor, Specialization, WorkingDay
from .serializers import DoctorSerializer, SpecializationSerializer, DoctorSerializerSet, WorkingDaySerializer
from authentication.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings
from django.db.models import Avg




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
    queryset = Doctor.objects.all().filter(is_confirmed=True)
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


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print("Request method:", request.method)
        if request.user.role != 'patient':
            return Response({"detail": "Only patients can create ratings."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            rating_instance = serializer.save() 
            self.update_average_rating(rating_instance.doctor)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        rating = self.get_object()  
        serializer = self.get_serializer(rating)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        rating = self.get_object() 
        if request.user.role != 'patient':
            return Response({"detail": "Only patients can update ratings."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(rating, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  
            self.update_average_rating(rating.doctor) 
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update_average_rating(self, doctor):
        avg_rating = doctor.ratings.aggregate(Avg('value'))['value__avg']
        doctor.average_rating = avg_rating if avg_rating is not None else 0.00
        doctor.save()
        
def search_doctors(request):
    department_name = request.GET.get('department', '')
    doctor_name = request.GET.get('doctor', '')

    doctors = Doctor.objects.all()

    if department_name:
        doctors = doctors.filter(specialization__title__icontains=department_name)

    if doctor_name:
        doctors = doctors.filter(
            Q(user__first_name__icontains=doctor_name) | Q(user__last_name__icontains=doctor_name)
        )

    results = []
    for doctor in doctors:
        working_days_list = list(doctor.working_days.values_list('id', flat=True))  # Convert working days to list
        result = {
            'id': doctor.id,
            'user__first_name': doctor.user.first_name,
            'user__last_name': doctor.user.last_name,
            'profile_picture': request.build_absolute_uri(settings.MEDIA_URL + doctor.profile_picture.name),
            'address': doctor.address,
            'price': doctor.price,
            'is_confirmed': doctor.is_confirmed,
            'working_days': working_days_list,  # Return working_days as a list of strings
            'average_rating': doctor.average_rating,
        }
        results.append(result)

    return JsonResponse(results, safe=False)



class WorkingDayViewSet(viewsets.ModelViewSet):
    queryset = WorkingDay.objects.all() 
    serializer_class = WorkingDaySerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role != 'patient':
            return Response({"detail": "Only patients can create comments."}, status=status.HTTP_403_FORBIDDEN)
        doctor_id = request.data.get('doctor')
        patient_id = request.user.id 
        
        if Comment.objects.filter(doctor_id=doctor_id, patient_id=patient_id).exists():
            return Response({"detail": "You can only comment once on this doctor."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = self.get_serializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
