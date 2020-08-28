from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    isCustomer = models.BooleanField(default=False)
    isPerformer = models.BooleanField(default=False)
    isFirm = models.BooleanField(default=False)
    @property
    def get_name(self):
        if self.isFirm:
            return self.firm.name
        return '%s %s' % (self.first_name, self.last_name)
    def __str__(self):
        if self.isFirm:
            return self.firm.name
        return '%s %s' % (self.first_name, self.last_name)

class Firm(models.Model):
    name = models.CharField(max_length=128, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_number = models.IntegerField(null=True)
    website = models.CharField(max_length=128,blank=True)
