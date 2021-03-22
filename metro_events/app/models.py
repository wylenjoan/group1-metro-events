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

    class Meta:
        db_table = "User"

class OrganizerUser(models.Model):
    regular_user_id = models.ForeignKey(RegularUser, on_delete=models.CASCADE, related_name='organizers')
    granted_at = models.DateTimeField(default = timezone.now)

    class Meta:
        db_table = "Organizer"

class AdministratorUser(models.Model):
    regular_user_id = models.ForeignKey(RegularUser, on_delete=models.CASCADE, related_name='administrators')
    granted_at = models.DateTimeField(default = timezone.now)

    class Meta:
        db_table = "Administrator"