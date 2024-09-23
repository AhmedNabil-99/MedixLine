from django.urls import path, include
from .views import PatientRegistrationView, PatientViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', PatientViewSet, basename='patient')

urlpatterns = [
    path('register/', PatientRegistrationView.as_view(), name='patient-registration'),
] + router.urls
