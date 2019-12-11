from order.services import order_status_style_dict, get_category_by_value
from performer.models import Performer
from order.models import OrderRespond, OrderRespondStatus, OrderStatus, Category, SubCategory
from location.models import OrderLocationType
from django import template

register = template.Library()


@register.simple_tag(name='is_respond_tag')
def already_respond(user, order):
    try:
        performer = Performer.objects.get(user=user)
    except Performer.DoesNotExist:
        return False
    return OrderRespond.objects.filter(order=order, performer=performer).exists()


@register.simple_tag(name='new_responds_tag')
def new_responds(order):
    return OrderRespond.objects.filter(order=order,
                                       status=OrderRespondStatus.getDafaultValue()).count()


@register.simple_tag(name='responds_tag')
def responds(order):
    return OrderRespond.objects.filter(order=order).count()


@register.simple_tag(name='order_status_style')
def order_status_style(order_status):
    return order_status_style_dict[OrderStatus.objects.get(name=order_status).pk]

@register.simple_tag(name='is_active')
def is_active(order):
    return order.status == OrderStatus.getDafaultValue()

@register.simple_tag(name='is_processing')
def is_processing(order):
    return order.status == OrderStatus.getProcessingValue()

@register.simple_tag(name='is_done')
def is_done(order):
    return order.status == OrderStatus.getDoneValue()

@register.simple_tag(name='get_performer')
def get_performer(order):
    pass

@register.simple_tag(name='get_categories')
def get_categories():
    return Category.objects.all()

@register.simple_tag(name='get_subcategories')
def get_subcategories(category_value):
    print(category_value)
    if category_value:
        category = get_category_by_value(category_value)
        if not category:
            return []

        return SubCategory.objects.filter(category=category)
    else:
        return []

@register.simple_tag(name='has_map')
def has_map(order):
    return order.order_location_type != OrderLocationType.getRemote()