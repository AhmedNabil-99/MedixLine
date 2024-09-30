from django.db import models
from authentication.models import User
import base64

from django.core.validators import RegexValidator,FileExtensionValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Specialization(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)
    image = models.ImageField(
        upload_to='specialization/images',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
        )

    def __str__(self):
        return self.title
    
class WorkingDay(models.Model):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    day = models.CharField(max_length=10, choices=DAY_CHOICES)

    def __str__(self):
        return self.day.capitalize()

class Doctor(models.Model):
    phone_number_validator = RegexValidator(
        regex=r'^(010|011|015|012)\d{8}$',
        message="Not A Valid Phone Number."
    )
    gender_choices = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]  

    gender = models.CharField(max_length=10, choices=gender_choices)

    address = models.TextField()

    
    description = models.TextField(
        null=True,
        blank=True
    )
    phone_number = models.CharField(
            max_length=11,
            validators=[phone_number_validator],
            unique=True
        )        
    profile_picture = models.ImageField(
        upload_to="doctors/images/profile_pic", 
        null=False, 
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    national_id = models.ImageField(
        upload_to="doctors/images/national_ids",
        null=False, 
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    syndicate_id = models.ImageField(
        upload_to="doctors/images/syndicate_ids", 
        null=False, 
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    is_confirmed = models.BooleanField(
        default=False
    )
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_account")
    working_days = models.ManyToManyField(WorkingDay, related_name="doctor_working_days", null=True, blank=True)
    start_time = models.TimeField(
        null=True,
        blank=True
    )
    end_time = models.TimeField(
        null=True,
        blank=True
        )
    duration = models.IntegerField(
        null=True,
        blank=True
    )
    price = models.IntegerField(
        null=True,
        blank=True
    )
    

    def __str__(self):
        return f"{self.user.username}"


    

