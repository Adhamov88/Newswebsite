from django.contrib import admin
from .models import User
# Register your models here.
from django.contrib import admin
from .models import Profile

class AdminProfile(admin.ModelAdmin):
    list_display = ['user','date_of_birth','photo' ]  # Replace 'other_field' with the actual names of other fields you want to display

admin.site.register(Profile, AdminProfile)