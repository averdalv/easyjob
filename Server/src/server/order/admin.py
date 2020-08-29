from django.contrib import admin

# Register your models here.
from order.models import SimpleOrder, OrderStatus,SubCategory,Category

admin.site.register(SimpleOrder)
admin.site.register(OrderStatus)
admin.site.register(SubCategory)
admin.site.register(Category)