from rest_framework import serializers
from .models import Doctor, Specialization, WorkingDay
from authentication.models import User
from authentication.serializers import UserSerializer


class DoctorSerializerSet(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Doctor
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        working_days_data = validated_data.pop('working_days', None)
        user_data['role'] = 'doctor'
        user = User.objects.create_user(**user_data)
        
        doctor = Doctor.objects.create(user=user, **validated_data)

        if working_days_data:
            doctor.working_days.set(working_days_data)
            
        return doctor

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class WorkingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingDay
        fields = '__all__'