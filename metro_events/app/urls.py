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
    # path('user-dashboard/events', views.UserDashboardEventsView.as_view(), name='user-dashboard-events'),
    # path('user-dashboard/profile', views.UserDashboardProfileView.as_view(), name='user-dashboard-profile'),

    path('/organizer-dashboard', views.OrganizerDashboardView.as_view(), name='organizer-dashboard'),
    # path('/organizer-dashboard/event-list', views.OrganizerDashboardView.as_view(), name='organizer-dashboard-event-list'),
    # path('/organizer-dashboard/join-requests', views.OrganizerDashboardView.as_view(), name='organizer-dashboard-event-list'),

    path('/admin-dashboard', views.AdminDashboardView.as_view(), name='admin-dashboard'),
    # path('/admin-dashboard/upgrade-request', views.AdminDashboardView.as_view(), name='admin-dashboard-upgrade-request'),
    # path('/admin-dashboard/event-request', views.AdminDashboardView.as_view(), name='admin-dashboard-event-request'),
    # path('/admin-dashboard/user-list', views.AdminDashboardView.as_view(), name='admin-dashboard-user-list'),
    # path('/admin-dashboard/event-list', views.AdminDashboardView.as_view(), name='admin-dashboard-event-list'),
]
