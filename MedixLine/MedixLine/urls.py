"""
URL configuration for MedixLine project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
<<<<<<< HEAD
from django.urls import path
from rest_framework.routers import DefaultRouter
from patients.views import PatientViewSet

router = DefaultRouter()
router.register(r'Api/Patient', PatientViewSet, basename='patient')

urlpatterns = [
    path('admin/', admin.site.urls),
] + router.urls
=======
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('doctors.urls')),
    path('api/auth/', include('authentication.urls')),
    ]
>>>>>>> 7f7c0be68e0415f216fd3dea2a08d9936b15f1f2
