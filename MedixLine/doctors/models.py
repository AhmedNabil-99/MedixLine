from django.db import models

# Create your models here.
class Specialization(models.Model):
    specialization = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.specialization

class Doctor(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    phone_number = models.CharField(max_length=11, null=False)
    email = models.EmailField(null=False)
    profile_picture = models.ImageField(upload_to="doctors/images/profile_pic", null=False)
    national_id = models.ImageField(upload_to="doctors/images/national_ids", null=False)
    syndicate_id = models.ImageField(upload_to="doctors/images/syndicate_ids", null=False)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, null=True)




    

