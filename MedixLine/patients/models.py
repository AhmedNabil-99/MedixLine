from django.db import models
from authentication.models import User
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

class Patient(models.Model):
    # other fields related to student ...
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender_choices = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]  
    phone_number_validator = RegexValidator(
        regex=r'^(010|011|015|012)\d{8}$',
        message="Not A Valid Phone Number."
    )
    gender = models.CharField(max_length=10, choices=gender_choices)
    phone_number = models.CharField(
        max_length=11,
        validators=[phone_number_validator],
        unique=True
    )    
    # email = models.EmailField(unique=True)
    address = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_account")

    def __str__(self):
        return f"{self.user.username}"

    def clean(self):
        super().clean()
        if self.date_of_birth and self.date_of_birth > timezone.now().date():
            raise ValidationError("Not A Valid Date of Birth")
    
