
from django import template

from chat.models import Message, Dialogue

register = template.Library()

@register.simple_tag(name='unread_messages_count')
def unread_messages_count(user):
    unread_messages = Message.objects.filter(messsage_to=user).filter(is_read=False).count()
    return unread_messages
