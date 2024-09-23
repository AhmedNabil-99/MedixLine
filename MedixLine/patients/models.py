# from django.db import models
# from django.contrib.auth.models import User


# # Create your models here.
# class Patient(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     date_of_birth = models.DateField()
#     gender = models.CharField(max_length=10)
#     phone_number = models.CharField(max_length=15)
#     email = models.EmailField()
#     address = models.TextField()


from django.db import models
from authentication.models import User

class Patient(models.Model):
    # other fields related to student ...
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_account")