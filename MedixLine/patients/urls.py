from django.urls import path, include
from .views import PatientRegistrationView, PatientViewSet, activate
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', PatientViewSet, basename='patient')

urlpatterns = [
    path('register/', PatientRegistrationView.as_view(), name='patient-registration'),
    path('activate/<uidb64>/', activate, name='activate-patient'),
] + router.urls
