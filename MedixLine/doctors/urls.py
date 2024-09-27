from django.urls import path
from . import views
from .views import DoctorRegistrationView, activate
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('specializations', views.SpecializationViewSet, basename = 'specializations')
router.register('', views.DoctorViewSet, basename= 'doctors')


urlpatterns = [
    path('register/', DoctorRegistrationView.as_view(), name='doctor-registration'),
    path('activate/<uidb64>/', activate, name='activate-doctor'),
]
urlpatterns = urlpatterns + router.urls
