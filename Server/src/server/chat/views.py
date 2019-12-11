from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View

from authentication.models import User

from chat.models import Dialogue, Message

from notifications.signals import notify

from server.services import NotificationType

from datetime import datetime


class ChatView(LoginRequiredMixin, View):
    def get(self, request):
        user_id = request.GET.get('user_id')
        active_id = -2
        if user_id and int(user_id) != request.user.id:
            user_to = User.objects.filter(id=user_id).first()
            dialogue = Dialogue.objects.filter(
                user_from=request.user).filter(user_to=user_to).first()
            if not dialogue:
                dialogue = Dialogue.objects.create(
                    user_from=request.user, user_to=user_to)
                active_id = dialogue.id
            else:
                active_id = dialogue.id
                dialogue.count_unread_messages = 0
                dialogue.save()
        dialogues = Dialogue.objects.filter(
            user_from=request.user).order_by('-date_last_message')
        if dialogues.count() == 0:
            active_id = -1
        context = {"dialogues": dialogues,
                   "active_id": active_id, "user_to_id": user_id}
        if user_id and int(user_id) != request.user.id:
            context["user_to_id"] = user_id
        if active_id != -1 and user_id and int(user_id) != request.user.id:
            messages = Message.objects.filter((Q(message_from=user_to) & Q(message_to=request.user)) | (
                Q(message_from=request.user) & Q(message_to=user_to))).order_by("date")
            messages.update(is_read=True)
            notifications = request.user.notifications.unread().filter(level=NotificationType.Message.value)
            for notification in notifications:
                if notification.actor == user_to:
                    notification.mark_as_read()
            context["messages"] = messages
        return render(request, "chat/chat.html", context)


class SendMessageView(View):
    def post(self, request):
        if not request.POST.get('to'):
            return JsonResponse({}, status=500)
        user_to_id = int(request.POST.get('to'))
        if user_to_id == -1 or user_to_id == request.user.id:
            return JsonResponse({}, status=500)
        user_to = User.objects.filter(id=user_to_id).first()
        if not user_to:
            return JsonResponse({}, status=500)
        message = request.POST.get("message")
        message = message.strip()
        if not message:
            return JsonResponse({}, status=500)
        dialogue_from = Dialogue.objects.filter(
            user_from=user_to).filter(user_to=request.user).first()
        if not dialogue_from:
            dialogue_from = Dialogue.objects.create(
                user_from=user_to, user_to=request.user)
        dialogue_from.last_message = message
        dialogue = Dialogue.objects.filter(
            user_to=user_to).filter(user_from=request.user).first()
        dialogue.last_message = message
        date = datetime.now()
        dialogue.date_last_message = date
        dialogue_from.date_last_message = date
        dialogue_from.count_unread_messages += 1
        dialogue.save()
        dialogue_from.save()
        Message.objects.create(
            message_from=request.user, text=message, message_to=user_to, date=datetime.now())
        message_data = [{'message_from': request.user.id, 'text': message,
                         'date': date.strftime("%H:%M"), 'message_to': user_to_id}]

        notify.send(request.user,
                    recipient=user_to,
                    img={'url':request.user.profile.profile_picture.url},
                    verb=message[:min(len(message), 25)],
                    level=NotificationType.Message.value)

        return JsonResponse(message_data, safe=False)


class GetMessagesView(View):
    def post(self, request):
        if not request.POST.get('to'):
            return JsonResponse({}, status=500)
        user_to_id = int(request.POST.get('to'))
        if user_to_id == -1 or user_to_id == request.user.id:
            return JsonResponse({}, status=500)
        user_to = User.objects.filter(id=user_to_id).first()
        if not user_to:
            return JsonResponse({}, status=500)
        messages = Message.objects.filter(
            message_from=user_to, message_to=request.user, is_read=False)
        if messages.count() > 0:
            dialogue = Dialogue.objects.filter(user_from=request.user,user_to=user_to).first()
            dialogue.count_unread_messages = 0
            dialogue.save()
        dialogues = Dialogue.objects.filter(user_from=request.user).filter(count_unread_messages__gt=0)
        messages_json = []
        notifications = request.user.notifications.unread().filter(level=NotificationType.Message.value)
        for notification in notifications:
            if notification.actor == user_to:
                notification.mark_as_read()
        for message in messages:
            messages_json.append({"message_from": message.message_from.id, 'text': message.text, 'date': message.date.strftime(
                "%H:%M"), 'img': message.message_from.profile.profile_picture.url})
        messages.update(is_read=True)
        dialogues_json = []
        for d in dialogues:
            dialogues_json.append({"href":d.get_absolute_url(),"count_unread":d.count_unread_messages,"date_last_message":d.date_last_message.strftime("%H:%M"),
                                   "last_message":d.last_message,"profile_picture_url":d.user_to.profile.profile_picture.url,"name":d.user_to.get_name})
        json_to_return = {"dialogues":dialogues_json,"messages":messages_json}
        return JsonResponse(json_to_return, safe=False)
