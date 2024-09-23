from django.db import models
from authentication.models import User


# Create your models here.
class Specialization(models.Model):
    specialization = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.specialization

class Doctor(models.Model):
    # first_name = models.CharField(max_length=50, null=False)
    # last_name = models.CharField(max_length=50, null=False)
    phone_number = models.CharField(max_length=11, null=False)
    # email = models.EmailField(null=False)
    profile_picture = models.ImageField(upload_to="doctors/images/profile_pic", null=True)
    national_id = models.ImageField(upload_to="doctors/images/national_ids", null=True)
    syndicate_id = models.ImageField(upload_to="doctors/images/syndicate_ids", null=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, null=True)

    # student_id = models.CharField(max_length=10, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_account")


    

