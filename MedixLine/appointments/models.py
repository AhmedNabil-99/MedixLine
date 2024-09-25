from django.db import models
from doctors.models import Doctor
from patients.models import Patient
from django.core.exceptions import ValidationError
from django.utils import timezone
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    patient= models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    doctor= models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"Appointment on {self.date} at {self.time} - Status: {self.get_status_display()}"
    
    def clean(self):
        super().clean()

        if self.date is None or self.time is None:
            raise ValidationError("Date and time must be provided.")
        appointment_datetime = timezone.make_aware(timezone.datetime.combine(self.date, self.time))
        now = timezone.now()
        if appointment_datetime < now:
            raise ValidationError("Appointment time cannot be in the past.")
    
