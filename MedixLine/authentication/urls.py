from django.urls import path
from .views import UserLoginView, UserLogoutView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
]