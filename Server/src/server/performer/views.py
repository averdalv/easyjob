from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View

from performer.models import Performer, PerformingSubCategory
from order.models import SimpleOrder, OrderRespond
from order.decorators import performer_required_dec

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from order.services import get_orders
from order.models import Category

class PerformerPage(View):
    def get(self, request, id):
        performer = get_object_or_404(Performer, id__iexact=id)
        performing_sub_categories = PerformingSubCategory.objects.filter(performer=performer)
        context = {"performer": performer,"performing_sub_categories":performing_sub_categories}
        return render(request, "performer/performer_page.html", context)


class Performers(View):
    def get(self, request):
        performers = Performer.objects.all()
        categories = Category.objects.all()
        context = {"performers": performers,"categories":categories}
        return render(request, "performer/performers.html", context)


class Candidates(View):
    @method_decorator(login_required)
    def get(self, request):
        id = request.GET.get('id')
        if not id:
            return HttpResponse(status=400)

        order = get_object_or_404(SimpleOrder, id=id)
        performer_id = OrderRespond.objects.filter(
            order=order).values_list('performer', flat=True)
        performers = Performer.objects.filter(id__in=list(performer_id))

        context = {"performers": performers,
                   "order": order}
        return render(request, "performer/candidates.html", context)


class PerformerOrders(View):
    def get(self, request):
        if request.user.isPerformer:
            status = request.GET.get('status', None)
            if status:
                status = get_object_or_404(OrderStatus, value=status)
            performer = get_object_or_404(Performer, user=request.user)

            responds = OrderRespond.objects.filter(performer=performer)

            # orders = [respond.order for respond in responds]

        else:
            responds = []
        
        return render(request, 'performer/performer_orders.html', {
            'responds': responds
        })

