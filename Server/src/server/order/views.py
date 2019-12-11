from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Count

from order.models import SimpleOrder, Category, SubCategory, OrderStatus, OrderRespond, OrderRespondStatus, Payment
from order.decorators import customer_required_dec, performer_required_dec
from order.services import get_orders, get_subcategories_by_category_value, get_category_by_value, get_subcategory_by_value, \
    is_valid_orders_order_by
from order.forms import SimpleOrderForm
from order.serializers import SimpleOrderSerializer

from customer.models import Customer

from performer.models import Performer

from gallery.models import GalleryImage, Gallery

from notifications.signals import notify

from server.services import NotificationType

from location.models import Location, City, OrderLocationType
from location.services import get_city_by_value

import uuid


class OrdersView(View):
    def get(self, request, category_value=None, sub_category_value=None):
        page = request.GET.get('page', 1)

        categories = []
        orders_count = 0

        categories_db = Category.objects.all()
        for category in categories_db:
            count = SimpleOrder.objects.filter(category=category).count()
            orders_count += count

            categories.append({
                'name': category.name,
                'value': category.value,
                'count': count})

        category = get_category_by_value(category_value)
        subcategory = get_subcategory_by_value(sub_category_value)

        orders = get_orders(category=category, subcategory=subcategory,
                            page=page, per_page=10, order_by='-time_created')

        return render(request, 'order/orders.html', {
            'orders': orders,
            'categories': categories,
            'orders_count': orders_count,
            'current_category': category,
            'current_subcategory': subcategory
        })


class OrdersJsonView(View):
    def get(self, request):
        user = request.user

        print(request.GET)

        page = request.GET.get('page', 1)
        category = request.GET.get('category', None)
        subcategory = request.GET.get('subcategory', None)
        city = request.GET.get('city', None)
        low = request.GET.get('low_price', None)
        high = request.GET.get('high_price', None)
        customer_type = request.GET.get('customer_type', None)
        remote = request.GET.get('remote', None)
        order_by =  request.GET.get('order_by', 'time_created')

        category = get_category_by_value(category)
        subcategory = get_subcategory_by_value(subcategory)
        city = get_city_by_value(city)

        if not is_valid_orders_order_by(order_by):
            order_by = 'time_created'

        print(category, subcategory, page, city, low, high)

        if customer_type is not None:
            if customer_type == "individual": 
                individual_only = True
            elif customer_type == "firm":
                individual_only = False
        else:
            individual_only = None

        if remote == "true":
            remote = True
        else:
            remote = False

        orders = get_orders(category=category, subcategory=subcategory,
                            page=page, per_page=10, order_by='-' + order_by,
                            city=city, low=low, high=high, individual_only=individual_only,
                            remote=remote)

        ret = {
            "orders": SimpleOrderSerializer(orders, user=user, many=True).data,
            "has_other_pages": orders.has_other_pages()
        }

        if orders.has_other_pages():
            ret["has_previous"] = orders.has_previous()
            ret["page_range"] = len(orders.paginator.page_range)
            ret["number"] = orders.number
            ret["has_next"] = orders.has_next()

            if orders.has_previous():
                ret["previous_page_number"] = orders.previous_page_number()

            if orders.has_next():
                ret["next_page_number"] = orders.next_page_number()

        return JsonResponse(ret, safe=False)


class OrderView(View):
    def get(self, request, id=None):
        order = get_object_or_404(SimpleOrder, id=id)
        order.views += 1
        order.save()
        print(order.price_low, order.price_high)
        galleryImages = GalleryImage.objects.filter(gallery=order.gallery)
        return render(request, 'order/order.html', {
            'order': order,
            'galleryImages': galleryImages
        })

class CitiesJsonView(View):
    @method_decorator(login_required)
    def get(self, request):
        cities = City.objects.annotate(count=Count('location__simpleorder__id')).order_by('-count')[:4]
        return JsonResponse(list(cities.values_list('name', 'value', 'count')), safe=False)

class CategoryJsonView(View):
    @method_decorator(login_required)
    def get(self, request):
        categories = Category.objects.annotate(count=Count('simpleorder__id')).order_by('-count')[:8]
        return JsonResponse(list(categories.values_list('name', 'value', 'count')), safe=False)

class SubCategoryJsonView(View):
    @method_decorator(login_required)
    def get(self, request):

        category_value = request.GET.get('category', 1)
        print("ggg", category_value)
        try:
            category = Category.objects.get(value=category_value)
        except Category.DoesNotExist:
            return JsonResponse([], safe=False)

        return JsonResponse(list(SubCategory.objects.filter(category=category).values()), safe=False)

class BookmarkOrderJsonView(View):
    @method_decorator(login_required)
    def get(self, request):
        order_id = request.GET.get('order_id', None)
        if not order_id:
            return JsonResponse("No order Id", safe=False)

        user = request.user
        is_bookmarked = user.profile.bookmarked_orders.filter(id=order_id).exists()
        return JsonResponse({"is_bookmarked": is_bookmarked}, safe=False)

    @method_decorator(login_required)
    def post(self, request):
        order_id = request.POST.get('order_id', None)
        if not order_id:
            return JsonResponse("No order Id", safe=False)
        
        user = request.user
        bookmark_order = user.profile.bookmarked_orders.filter(id=order_id).exists()
        if bookmark_order:
            return JsonResponse("Already bookmarked", safe=False)
        
        order = get_object_or_404(SimpleOrder, id=order_id)
        user.profile.bookmarked_orders.add(order)

        return JsonResponse("OK", safe=False)


class AddOrderView(View):
    # @method_decorator(customer_required_dec)
    @method_decorator(login_required)
    def post(self, request):
        simple_order_form = SimpleOrderForm(data=request.POST)

        user = request.user

        print("user", user)
        print(request.POST)

        uuid = request.POST['uuid']

        category_value = request.POST['category']
        subcategories = get_subcategories_by_category_value(category_value)
        simple_order_form.fields['subcategory'].choices = list(
            subcategories.values_list('value', 'value'))
        order_location_type = request.POST['order_location_type']

        if simple_order_form.is_valid() and uuid:
            simple_order = simple_order_form.save(commit=False)

            try:
                simple_order.customer = Customer.objects.get(user=user)
            except Customer.DoesNotExist:
                simple_order.customer = None

            gallery = Gallery()
            gallery.save()

            simple_order.gallery = gallery
            simple_order.status = OrderStatus.getDafaultValue()

            if order_location_type == "in-customer":
                address = request.POST['location']
                lat_value = float(request.POST['lat'])
                lon_value = float(request.POST['lon'])
                city = City.objects.get(value=request.POST['city'])
                location = Location(city=city, lon=lon_value,
                                    lat=lat_value, address=address)
                location.save()
                simple_order.location = location
            elif order_location_type == "in-performer":
                city = City.objects.get(value=request.POST['city'])
                location = Location(city=city, lon=city.lon,
                                    lat=city.lat)
                location.save()
                simple_order.location = location
            elif order_location_type == "in-remote":
                pass

            galleryImages = GalleryImage.objects.filter(gallery_uuid=uuid)
            for galleryImage in galleryImages:
                galleryImage.gallery = gallery
                galleryImage.save()

            if request.FILES.__contains__("order_image_preview"):
                # os.path.join(request.FILES['order_image_preview'],simple_order.name+str(simple_order.time_created))
                simple_order.order_image_preview = request.FILES['order_image_preview']
            
            simple_order.save()
        else:
            print(simple_order_form.errors)

        return redirect('order_app:orders')

    # @method_decorator(customer_required_dec)
    def get(self, request):
        simple_order_form = SimpleOrderForm()
        return render(request, 'order/add_order.html',
                      {'simple_order_form': simple_order_form,
                       'uuid': uuid.uuid4()})


class UploadGalleryPhotoView(View):
    def post(self, request):
        file = request.FILES['file']
        uuid = request.POST['uuid']
        if file and uuid:
            galleryImage = GalleryImage(name=str(file),
                                        image=file,
                                        thumb=file,
                                        gallery_uuid=uuid)

            galleryImage.save()

            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)


class OrderRespondView(View):
    @method_decorator(performer_required_dec)
    def post(self, request):
        if request.user.isPerformer:
            user = request.user
            id = request.POST['id']

            order = get_object_or_404(SimpleOrder, id=id)
            performer = get_object_or_404(Performer, user=user)

            # Check if current user already respond to this order
            # (button must be unavalible)

            if OrderRespond.objects.filter(order=order, performer=performer).exists():
                print("Wrong")

                return HttpResponse(status=500)
                # Mistake

            order_respond = OrderRespond(order=order,
                                         customer=order.customer,
                                         performer=performer,
                                         status=OrderRespondStatus.getDafaultValue())

            order_respond.save()

            notify.send(performer.user,
                        recipient=order.customer.user,
                        verb='',
                        order={'id': order.id,
                               'name': order.name},
                        notify_type="new_respond",
                        level=NotificationType.Notification.value)

        return redirect('order_app:orders')


class OrderConfirmView(View):
    @method_decorator(customer_required_dec)
    def post(self, request):
        performer_id = request.POST['performer_id']
        order_id = request.POST['order_id']

        if not performer_id or not order_id:
            return HttpResponse(status=404)

        performer = get_object_or_404(Performer, id=performer_id)
        customer = get_object_or_404(Customer, user=request.user)
        order = get_object_or_404(SimpleOrder, id=order_id)

        all_responds = OrderRespond.objects.filter(
            customer=customer, order=order)
        accepted_respond = get_object_or_404(all_responds, performer=performer)
        rejected_responds = all_responds.exclude(id=accepted_respond.id)

        for respond in rejected_responds:
            respond.status = OrderRespondStatus.getRejectedValue()
            respond.save()

        accepted_respond.status = OrderRespondStatus.getAcceptedValue()
        accepted_respond.save()

        order.performer = performer
        order.status = OrderStatus.getProcessingValue()
        order.save()

        notify.send(customer.user,
                    recipient=performer.user,
                    verb='',
                    order={'id': order.id,
                           'name': order.name},
                    notify_type="confirmed_respond",
                    level=NotificationType.Notification.value)

        return HttpResponse(status=200)
