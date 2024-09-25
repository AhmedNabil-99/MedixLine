from django.db import models
from authentication.models import User
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Patient(models.Model):
    date_of_birth = models.DateField()
    gender_choices = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]  
    phone_number_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits."
    )
    gender = models.CharField(max_length=10, choices=gender_choices)
    phone_number = models.CharField(
        max_length=10,
        validators=[phone_number_validator],
        unique=True
    )    
    email = models.EmailField(unique=True)
    address = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_account")

    def __str__(self):
        return f"{self.user.username}"

    def clean(self):
        super().clean()
        if self.date_of_birth > timezone.now().date():
            raise ValidationError("Not A Valid Date of Birth")
    
