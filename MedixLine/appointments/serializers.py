from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'date', 'time', 'patient', 'doctor','status']

    def create(self, validated_data):
        validated_data['status'] = 'pending'
        appointment = Appointment.objects.create(**validated_data)
        return appointment
    
    def update(self, instance, validated_data):
        instance.date = validated_data.get('date', instance.date)
        instance.time = validated_data.get('time', instance.time)
        instance.patient = validated_data.get('patient', instance.patient)
        instance.doctor = validated_data.get('doctor', instance.doctor)
        
        if 'status' in validated_data:
            instance.status = validated_data['status']
        
        instance.save()
        return instance