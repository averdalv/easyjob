from django.shortcuts import render

from django.http import JsonResponse
from django.forms import model_to_dict

from notifications.settings import get_config
from notifications.utils import id2slug

from server.services import NotificationType
from performer.models import Performer

def index(request):
    performers = Performer.objects.all()
    return render(request, 'index.html',{"performers":performers})

# To service
def build_notification_data(user, notification_type, num_to_fetch, mark_as_read):
    unread_list = []
    data = user.notifications.unread().filter(level=notification_type)
    for notification in data[0:num_to_fetch]:
        struct = model_to_dict(notification)
        struct['slug'] = id2slug(notification.id)
        if notification.actor:
            struct['actor'] = str(notification.actor)
        if notification.target:
            struct['target'] = str(notification.target)
        if notification.action_object:
            struct['action_object'] = str(notification.action_object)
        if notification.data:
            struct['data'] = notification.data

        if mark_as_read:
            notification.mark_as_read()

        unread_list.append(struct)

    return (unread_list, data.count())


def notifications_handler(request):
    ''' Return a json with a unread notification list '''
    try:
        user_is_authenticated = request.user.is_authenticated()
    except TypeError:  # Django >= 1.11
        user_is_authenticated = request.user.is_authenticated

    if not user_is_authenticated:
        data = {
            'unread_count_notifications': 0,
            'unread_list_notifications': []
        }
        return JsonResponse(data)

    default_num_to_fetch = get_config()['NUM_TO_FETCH']
    try:
        # If they don't specify, make it 5.
        num_to_fetch = request.GET.get('max', default_num_to_fetch)
        num_to_fetch = int(num_to_fetch)
        if not (1 <= num_to_fetch <= 100):
            num_to_fetch = default_num_to_fetch
    except ValueError:  # If casting to an int fails.
        num_to_fetch = default_num_to_fetch

    unread_notifications = build_notification_data(user=request.user,
                                                   notification_type=NotificationType.Notification.value,
                                                   num_to_fetch=num_to_fetch,
                                                   mark_as_read=request.GET.get('mark_as_read'))

    unread_messages = build_notification_data(user=request.user,
                                              notification_type=NotificationType.Message.value,
                                              num_to_fetch=num_to_fetch,
                                              mark_as_read=request.GET.get('mark_as_read'))

    data = {
        'unread_count_notifications': unread_notifications[1],
        'unread_list_notifications': unread_notifications[0],
        'unread_count_messages': unread_messages[1],
        'unread_list_messages': unread_messages[0]
    }
    return JsonResponse(data)
