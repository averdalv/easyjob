from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from order.models import SimpleOrder, OrderStatus, Category, SubCategory, OrderLocationType

from django.db.models import Q


def get_category_by_value(category_value):
    try:
        category = Category.objects.get(value=category_value)
    except Category.DoesNotExist:
        category = None

    return category


def get_subcategory_by_value(subcategory_value):
    try:
        subcategory = SubCategory.objects.get(value=subcategory_value)
    except SubCategory.DoesNotExist:
        subcategory = None

    return subcategory


def get_orders(category=None, subcategory=None, status=None, customer=None, performer=None, page=1, per_page=2, order_by=None, city=None, low=None, high=None, individual_only=None, remote=None):
    orders = SimpleOrder.objects

    if category:
        orders = orders.filter(category=category)

    if subcategory:
        orders = orders.filter(subcategory=subcategory)

    if status:
        orders = orders.filter(status=status)

    if customer:
        orders = orders.filter(customer=customer)

    if performer:
        orders = orders.filter(performer=performer)

    if order_by:
        orders = orders.order_by(order_by)

    if city:
        orders = orders.filter(location__city=city)

    if individual_only is not None:
        orders = orders.filter(~Q(customer__user__isFirm=individual_only))

    if low:
        orders = orders.filter(price_high__gte=low)

    if high:
        orders = orders.filter(
            Q(Q(is_fixed_price=False) & Q(price_low__lte=high)) |
            Q(Q(is_fixed_price=True) & Q(price_high__lte=high))
        )

    if remote:
        orders = orders.filter(order_location_type=OrderLocationType.getRemote())

    paginator = Paginator(orders.all(), per_page)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    return orders


def get_subcategories_by_category_value(category_value):
    category = Category.objects.get(value=category_value)
    subcategories = SubCategory.objects.filter(category=category)
    return subcategories

def is_valid_orders_order_by(order_by):
    return order_by == "time_created"

order_status_style_dict = {
    1: "yellow",
    2: "green",
    3: "blue",
    4: "red"
}
