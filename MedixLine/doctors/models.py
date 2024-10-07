from django.db import models
from authentication.models import User
from patients.models import Patient
import base64
from django.utils import timezone
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


def validate_date_of_birth(date):
    if date and date > timezone.now().date():
            raise ValidationError("not a valid date of birth")

class Doctor(models.Model):
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    date_of_birth = models.DateField(
            validators=[validate_date_of_birth]
        )
    
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

    address = models.TextField(null=True, blank=True)

    
    description = models.TextField(
        null=True,
        blank=True
    )
    phone_number = models.CharField(
            max_length=11,
            validators=[phone_number_validator],
            unique=True,
            null=True,
            blank=True
        )        
    profile_picture = models.ImageField(
        upload_to="doctors/images/profile_pic", 
        null=False, 
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
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
    working_days = models.ManyToManyField(WorkingDay, related_name="doctor_working_days", blank=True)
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
        
    def update_average_rating(self):
        avg_rating = self.ratings.aggregate(Avg('value'))['value__avg']
        if avg_rating is not None:
            self.average_rating = avg_rating
        else:
            self.average_rating = 0.00
        self.save()

class Rating(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='ratings')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)]) 

    class Meta:
        unique_together = ('doctor', 'patient')

    def __str__(self):
        return f'{self.value} stars for {self.doctor.user.first_name}'

class Comment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='comments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'patient')

    def __str__(self):
        return f'{self.value} stars for {self.doctor.user.first_name}'
    

