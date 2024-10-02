from django.contrib import admin
from doctors.models import Specialization, Doctor, WorkingDay,Rating

# Register your models here.

admin.site.register(Specialization)  
admin.site.register(Doctor)
admin.site.register(WorkingDay)
admin.site.register(Rating)