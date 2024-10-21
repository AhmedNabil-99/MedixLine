from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from rest_framework import viewsets
from .models import Appointment
# from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin


# Create your views here.
class AppointmentsListView(APIView):
    def get(self,req):
        appointments=Appointment.objects.all()
        serializer=AppointmentSerializer(appointments,many=True)
        return Response(serializer.data)

class EachAppointment(APIView):
    def post(self,req):
        doctor_id = req.data.get('doctor')
        date = req.data.get('date')
        time = req.data.get('time')
        existing_appointment = Appointment.objects.filter(doctor_id=doctor_id, date=date, time=time).exists()

        if existing_appointment:
            return Response({'error': 'This slot is already booked.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AppointmentSerializer(data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,req,id):
        appointment = get_object_or_404(Appointment, pk=id)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def delete(self,req,id):
        appointment=get_object_or_404(Appointment,pk=id)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, req, id):
        appointment = get_object_or_404(Appointment, pk=id)
        serializer = AppointmentSerializer(appointment, data=req.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

