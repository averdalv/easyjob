from django.contrib import admin

from .models import Performer, PerformingSubCategory, Language, Education

admin.site.register(Performer)
admin.site.register(PerformingSubCategory)
admin.site.register(Language)
admin.site.register(Education)