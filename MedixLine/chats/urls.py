from django.urls import path
from . import views

urlpatterns = [
    path('my-inbox/<int:user_id>/', views.MyInbox.as_view(), name='my-inbox'),
    path('messages/<int:sender_id>/<int:reciever_id>/', views.GetMessages.as_view(), name='get-messages'),
    path('send-message/', views.SendMessage.as_view(), name='send-message'),
    path('profile/<int:pk>/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('search-user/<str:username>/', views.SearchUser.as_view(), name='search-user'),
]