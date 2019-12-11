from django.urls import path

from customer.views import CustomerOrders

app_name = 'customer_app'

urlpatterns = [
    path('orders', CustomerOrders.as_view(), name='orders'),
]
