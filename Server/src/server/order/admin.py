from django.contrib import admin

# Register your models here.
from order.models import SimpleOrder, OrderStatus

admin.site.register(SimpleOrder)
admin.site.register(OrderStatus)