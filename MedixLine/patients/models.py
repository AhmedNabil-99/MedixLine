from django.db import models
from authentication.models import User
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_date_of_birth(date):
    if date and date > timezone.now().date():
            raise ValidationError("not a valid date of birth")

class Patient(models.Model):
    date_of_birth = models.DateField(
        validators=[validate_date_of_birth]
    )

    phone_number_validator = RegexValidator(
        regex=r'^(010|011|015|012)\d{8}$',
        message="Please enter a valid egyptian phone number."
    )
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(
        max_length=11,
        validators=[phone_number_validator],
        unique=True,
        null=True,
        blank=True
    )    
    address = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_account")

    def __str__(self):
        return f"{self.user.username}"
    