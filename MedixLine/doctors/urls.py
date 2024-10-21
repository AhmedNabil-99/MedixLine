from django.urls import path
from . import views
from .views import DoctorRegistrationView, activate,RatingViewSet,CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('specializations', views.SpecializationViewSet, basename = 'specializations')
router.register('workingdays', views.WorkingDayViewSet, basename = 'workingdays')
router.register('ratings', views.RatingViewSet, basename='ratings')
router.register('comments', views.CommentViewSet, basename='comments')
router.register('', views.DoctorViewSet, basename= 'doctors')


urlpatterns = [
    path('register/', DoctorRegistrationView.as_view(), name='doctor-registration'),
    path('activate/<uidb64>/', activate, name='activate-doctor'),
    path('search/', views.search_doctors, name='search_doctors'),
]
urlpatterns = urlpatterns + router.urls
