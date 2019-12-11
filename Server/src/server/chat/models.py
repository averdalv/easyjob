from datetime import datetime, timedelta

from django.db import models
from django.urls import reverse

from authentication.models import User


class Dialogue(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_from')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_to')
    date_last_message = models.DateTimeField(default=datetime.now)
    last_message = models.CharField(max_length=256,blank=True)
    count_unread_messages = models.IntegerField(default=0)
    def __str__(self):
        return "User: " + self.user_from.last_name+" dialogue with: "+self.user_to.last_name

    @property
    def is_today(self):
        return datetime.now().date() == self.date_last_message.date()

    @property
    def is_yesterday(self):
        yesterday = datetime.now().date() - timedelta(days = 1)
        return yesterday == self.date_last_message.date()

    def get_absolute_url(self):
        return "/chat?user_id="+str(self.user_to.id)
class Message(models.Model):
    message_from = models.ForeignKey(User,on_delete=models.CASCADE, related_name='message_from')
    message_to = models.ForeignKey(User,on_delete=models.CASCADE, related_name='message_to')
    text = models.CharField(max_length=256)
    date = models.DateTimeField(default=datetime.now)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return "From: " + self.message_from.last_name+"|Date: "+str(self.date) + " |Message: " + self.text

    @property
    def is_today(self):
        return datetime.now().date() == self.date.date()