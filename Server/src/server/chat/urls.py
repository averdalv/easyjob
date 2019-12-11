from django.urls import path

from chat.views import ChatView, SendMessageView, GetMessagesView

app_name = 'chat_app'

urlpatterns = [
    path('send_message/', SendMessageView.as_view(), name='send_message'),
    path('get_messages/', GetMessagesView.as_view(), name='get_messages'),
    #path(r'^(?P<user_id>[-\w]+)$',ChatView.as_view(), name='chat')
    path('', ChatView.as_view(), name='chat'),
]
