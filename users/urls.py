from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('Welcome/', views.Welcome, name='Welcome'),
    path('profile/', views.profile, name='profile')  
]