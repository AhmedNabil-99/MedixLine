from django.shortcuts import render
from rest_framework import viewsets
from .models import Doctor, Specialization
from .serializers import DoctorSerializer, SpecializationSerializer

# Create your views here.
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all() 
    serializer_class = SpecializationSerializer