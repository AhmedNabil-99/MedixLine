from django.contrib import admin
from doctors.models import Specialization, Doctor, WorkingDay

# Register your models here.

admin.site.register(Specialization)  
admin.site.register(Doctor)
admin.site.register(WorkingDay)