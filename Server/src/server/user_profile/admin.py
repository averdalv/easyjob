from django.contrib import admin

# Register your models here.
from user_profile.models import Profile

admin.site.register(Profile)