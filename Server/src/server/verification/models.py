from datetime import datetime

from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from authentication.models import User


class EmailVerification(models.Model):
    is_verified = models.BooleanField(default=False)
    is_sent_link = models.BooleanField(default=False)
    time_sent_link = models.DateTimeField(default=datetime.now,null=True)
class BaseVerification(models.Model):
    email_verification = models.ForeignKey(to=EmailVerification,on_delete=models.CASCADE,null=True)
    # phone_verification = models.ForeignKey(to=PhoneVerification,on_delete=models.CASCADE)
    # phone_verification = models.ForeignKey(to=PassportVerification, on_delete=models.CASCADE)
    @property
    def is_email_verified(self):
        return self.email_verification.is_verified

    @property
    def is_phone_verified(self):
        return False
        # return self.phone_verification.is_verified

    @property
    def is_passport_verified(self):
        return False
        # return self.passport_verification.is_verified
class PerformerVerification(BaseVerification):
    # education_verification = models.ForeignKey(to=EducationVerification,on_delete=models.CASCADE)
    performer = models.OneToOneField(to='performer.Performer',on_delete=models.CASCADE,related_name='verification')
    @property
    def is_education_verified(self):
        return False
        # return self.education_verification.is_verified
    def __str__(self):
        return self.performer.user.get_name

class CustomerVerification(BaseVerification):
    pass

class FirmVerification(BaseVerification):
    # document_verification = models.ForeignKey(to=DocumentVerification,on_delete=models.CASCADE)
    @property
    def is_document_verified(self):
        return False
        # return self.document_verification.is_verified



@receiver(post_save, sender=PerformerVerification)
def create_email_verification_performer(sender, instance, created, **kwargs):
    if created:
        obj = EmailVerification.objects.create()
        instance.email_verification = obj
        instance.save()


# @receiver(post_save, sender=PerformerVerification)
# def save_email_verification_performer(sender, instance, **kwargs):
#     instance.email_verification.save()