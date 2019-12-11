from django.contrib import admin

# Register your models here.
from chat.models import Message, Dialogue

admin.site.register(Message)
admin.site.register(Dialogue)