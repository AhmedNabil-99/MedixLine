from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('doctors', views.DoctorViewSet, basename= 'doctors')
router.register('specializations', views.SpecializationViewSet, basename = 'specializations')

urlpatterns = []
urlpatterns = urlpatterns + router.urls
