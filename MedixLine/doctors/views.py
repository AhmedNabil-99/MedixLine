from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Doctor, Specialization
from .serializers import DoctorSerializer, SpecializationSerializer, DoctorSerializerSet

# Create your views here.
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializerSet

class DoctorRegistrationView(APIView):
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all() 
    serializer_class = SpecializationSerializer