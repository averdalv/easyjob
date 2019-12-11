from django.contrib import admin

# Register your models here.
from location.models import Location, City

admin.site.register(Location)
admin.site.register(City)