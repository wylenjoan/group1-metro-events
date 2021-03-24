# Date Started: March 20, 2021
# Author/s: Wylen Joan Lee

# References:
#   https://docs.djangoproject.com/en/3.1/ref/models/fields/
#   https://docs.djangoproject.com/en/3.1/topics/db/queries/#backwards-related-objects

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class RegularUser(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.CharField(max_length = 6, blank = True, null = True)
    created_at = models.DateTimeField(default = timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_organizer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "User"

class OrganizerUser(models.Model):
    regular_user_id = models.ForeignKey(RegularUser, on_delete=models.CASCADE, related_name='organizer')
    granted_at = models.DateTimeField(default = timezone.now)

    class Meta:
        db_table = "Organizer"

class AdministratorUser(models.Model):
    regular_user_id = models.ForeignKey(RegularUser, on_delete=models.CASCADE, related_name='administrator')
    granted_at = models.DateTimeField(default = timezone.now)

    class Meta:
        db_table = "Administrator"

class Event(models.Model):
    title = models.CharField(max_length = 128, default = "", blank = True, null = True)
    description = models.CharField(max_length = 255, default = "", blank = True, null = True)
    event_type  = models.CharField(max_length = 128, default = "", blank = True, null = True)
    start_datetime = models.DateTimeField(default = timezone.now)
    end_datetime = models.DateTimeField(default = timezone.now)
    is_approved = models.BooleanField(default=False)
    upvotes_count = models.IntegerField(default = 0)
    street = models.CharField(max_length = 128, default = "", blank = True, null = True)
    city = models.CharField(max_length = 128, default = "", blank = True, null = True)
    province = models.CharField(max_length = 128, default = "", blank = True, null = True)

    organizer_id = models.ForeignKey(OrganizerUser, on_delete=models.CASCADE, related_name='organizer', blank = True, null = True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "Event"

class Request(models.Model):
    request_type = models.CharField(max_length = 128, default = "", blank = True, null = True)
    # possible request_type: upgrade, join_event, create_event

    user_id = models.ForeignKey(RegularUser, on_delete=models.CASCADE, related_name='sender')

    # for upgrade
    user_type = models.CharField(max_length = 128, default = "", blank = True, null = True)
    # possible user_type: organizer, admin
    
    # for join_event
    # for create_event
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='events', blank=True, null=True)

    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default = timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Request"