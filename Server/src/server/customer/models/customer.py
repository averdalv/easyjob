from django.db import models

from authentication.models import User
from customer.models.enums import CustomerCategoryChoices


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_type = models.CharField(
        max_length=128,
        choices=CustomerCategoryChoices
    )
    def __str__(self):
        return self.user.last_name + " " + self.user.first_name

    # todo contacts
