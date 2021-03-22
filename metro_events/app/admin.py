from django.contrib import admin
from .models import RegularUser, OrganizerUser, AdministratorUser

# Register your models here.
admin.site.register(RegularUser)
admin.site.register(OrganizerUser)
admin.site.register(AdministratorUser)