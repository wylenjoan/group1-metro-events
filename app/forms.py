# References:
# 

from django import forms
from .models import RegularUser, Event
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    user_id = forms.ModelChoiceField(queryset=User.objects.all(),required=False)
    gender = forms.CharField(required=False)
    is_organizer = forms.BooleanField(required=False)
    is_admin = forms.BooleanField(required=False)

    class Meta:
        model = RegularUser
        fields = ['user_id','gender','is_organizer','is_admin']