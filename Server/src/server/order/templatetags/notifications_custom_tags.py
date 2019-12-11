from performer.models import Performer
from order.models import OrderRespond, OrderRespondStatus, OrderStatus, Category, SubCategory
from django import template

register = template.Library()

@register.simple_tag(name='notifications_cnt')
def notifications_cnt(user, level):
    if user.is_authenticated:
        return user.notifications.unread().filter(level=level).count()
    else:
        return None
