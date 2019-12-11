from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from authentication.models import User
from verification.models import PerformerVerification


class Education(models.Model):
    HE = "higher_education"
    SE = "secondary_education"
    SPE = "special_education"
    EDUCATION_CHOICES = (
        (HE,"Высшее образование"),
        (SE,"Среднее образование"),
        (SPE,"Специальное образование")
    )
    EUDCATION_MAP = {
        HE:"Высшее образование",
        SE:"Среднее образование",
        SPE:"Специальное образование"
    }
    education_type = models.CharField(max_length=32,choices=EDUCATION_CHOICES,default=HE,null=False)
    educational_institution_name = models.CharField(max_length=128,null=False)
    def __str__(self):
        return self.education_type + " - " + self.educational_institution_name

    @property
    def get_education_type(self):
        return self.EUDCATION_MAP[self.education_type]

class Language(models.Model):
    name = models.CharField(max_length=256, blank=False)
    value = models.CharField(max_length=256, blank=False)
    def __str__(self):
        return self.name

class Performer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    education = models.ForeignKey(to=Education,null=True,on_delete=models.SET_NULL)
    languages = models.ManyToManyField(Language)
    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("performer_app:performer_page", kwargs={"id": self.id})




class PerformingSubCategory(models.Model):
    performer = models.ForeignKey(to=Performer,on_delete=models.CASCADE,null=False)
    price = models.IntegerField(null=True,blank=True)
    sub_category = models.ForeignKey(to='order.SubCategory',on_delete=models.CASCADE,null=False)
    is_price_negotiated = models.BooleanField(default=False)

    def __str__(self):
        return self.performer.user.get_name() + "-" + self.sub_category.name

@receiver(post_save, sender=Performer)
def create_verification_performer(sender, instance, created, **kwargs):
    if created:
        PerformerVerification.objects.create(performer=instance)

