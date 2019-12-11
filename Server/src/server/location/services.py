from location.models import City


def get_cities():
    return City.objects.all()


def get_city_by_value(city_value):
    try:
        city = City.objects.get(value=city_value)
    except City.DoesNotExist:
        city = None

    return city
