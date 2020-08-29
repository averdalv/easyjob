import os
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from authentication.models import User

from django.core.cache import cache
import datetime
import server.settings

from location.models import Location
from server.tools import disable_for_loaddata
from order.models import SimpleOrder

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=1, blank=True)  # 'm' or 'f'
    phone_number = models.CharField(max_length=13, blank=True)
    location = models.ForeignKey(to=Location, on_delete=models.CASCADE,null=True)

    bookmarked_orders = models.ManyToManyField(SimpleOrder)

    def image_folder(self, filename):
        filename = str(self.user.id) + '.' + filename.split('.')[1]
        path = "profile_pictures/{0}/{1}".format(self.user.id, filename)
        file_path = os.path.join(os.path.abspath(settings.MEDIA_ROOT),path)
        if os.path.isfile(file_path):
            os.remove(file_path)
        return path
    profile_picture = models.ImageField(upload_to=image_folder, blank=True)

    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                    seconds=server.settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    @property
    def is_email_verified(self):
        """if self.user.isPerformer:
            return self.user.performer.verification.is_email_verified
        else:
            return False"""
        return False

    @property
    def is_passport_verified(self):
        if self.user.isPerformer:
            # return self.user.performer.verification.is_passport_verified
            return True
        else:
            return False
    def set_email_verified(self):
        if self.user.isPerformer:
            self.user.performer.verification.email_verification.is_verified = True
            self.user.performer.verification.email_verification.save()

@receiver(post_save, sender=User)
@disable_for_loaddata
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
@disable_for_loaddata
def save_user_profile(sender, instance, **kwargs):
    if instance.profile is not None:
        instance.profile.save()