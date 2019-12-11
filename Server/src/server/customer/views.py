from django.shortcuts import render
from django.views.generic import View
from customer.models import Customer
from order.models import OrderStatus
from django.shortcuts import redirect, get_object_or_404

from order.services import get_orders

class CustomerOrders(View):
    def get(self, request):
        if request.user.isCustomer:
            status = request.GET.get('status', None)
            if status:
                status = get_object_or_404(OrderStatus, value=status)
            customer = get_object_or_404(Customer, user=request.user)
            orders = get_orders(status=status, customer=customer, per_page=100) # tmp
        else:
            orders = []
        
        return render(request, 'customer/customer_orders.html', {
            'orders': orders
        })