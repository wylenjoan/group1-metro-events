# Date Started: March 20, 2021
# Author/s: Wylen Joan Lee

# References:
# 

from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path('', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),

    path('user-dashboard/', views.UserDashboardView.as_view(), name='user-dashboard'),

    path('organizer-dashboard/', views.OrganizerDashboardView.as_view(), name='organizer-dashboard'),

    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
]