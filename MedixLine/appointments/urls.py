from django.urls import path
from .views import *

urlpatterns=[
    path('all/', AppointmentsListView.as_view(), name='appointmentsList'),
    path('<int:id>/', EachAppointment.as_view(), name='appointmentDetail'),  
    path('', EachAppointment.as_view(), name='createAppointment'),
]