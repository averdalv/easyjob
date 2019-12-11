from location.models import City
from django import template

register = template.Library()

@register.simple_tag(name='get_cities')
def get_cities():
    return City.objects.all()