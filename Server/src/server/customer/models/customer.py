from django.db import models

from authentication.models import User
from customer.models.enums import CustomerCategoryChoices


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    def __str__(self):
        return self.user.last_name + " " + self.user.first_name

    # todo contacts
