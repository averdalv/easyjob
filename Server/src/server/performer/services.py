from performer.models import Language


def get_language_by_value(language_value):
    try:
        language = Language.objects.get(value=language_value)
    except Language.DoesNotExist:
        language = None

    return language