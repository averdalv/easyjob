from django.db import models

from customer.models import Customer
from performer.models import Performer
from gallery.models import Gallery
from location.models import Location, OrderLocationType

from datetime import datetime


class BaseOrder(models.Model):
    pass


class Category(models.Model):
    name = models.CharField(max_length=256, blank=False)
    value = models.CharField(max_length=256, blank=False)
    # category picture

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=256, blank=False)
    value = models.CharField(max_length=256, blank=False)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class OrderStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, blank=False)
    value = models.CharField(max_length=256, blank=False)

    @staticmethod
    def getDafaultValue():
        return OrderStatus.objects.get(value="active")

    @staticmethod
    def getProcessingValue():
        return OrderStatus.objects.get(value="processing")

    @staticmethod
    def getDoneValue():
        return OrderStatus.objects.get(value="done")

    @staticmethod
    def getCanceledValue():
        return OrderStatus.objects.get(value="canceled")

    def __str__(self):
        return self.name


class Payment(models.Model):
    name = models.CharField(max_length=256, blank=False)
    value = models.CharField(max_length=256, blank=False)

    def __str__(self):
        return self.name


class SimpleOrder(BaseOrder):
    name = models.CharField(max_length=255)

    time_start = models.DateTimeField()
    time_end = models.DateTimeField()

    order_image_preview = models.ImageField(
        upload_to='order_image_preview', blank=True)

    is_fixed_price = models.BooleanField()
    price_low = models.FloatField(null=True)
    price_high = models.FloatField()

    description = models.TextField()

    time_created = models.DateTimeField(default=datetime.now, blank=True)
    rating = models.FloatField(default=0)
    views = models.IntegerField(default=0)

    gallery = models.ForeignKey(
        to=Gallery, on_delete=models.CASCADE, null=True, blank=True)

    # Location
    order_location_type = models.ForeignKey(
        to=OrderLocationType, on_delete=models.CASCADE)
    location = models.ForeignKey(
        to=Location, on_delete=models.CASCADE, null=True)

    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(
        to=SubCategory, on_delete=models.CASCADE, null=True)

    status = models.ForeignKey(
        to=OrderStatus, on_delete=models.CASCADE, null=False, blank=False)

    payment = models.ForeignKey(
        to=Payment, null=False, on_delete=models.CASCADE)

    performer = models.ForeignKey(
        to='performer.Performer', on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(
        to=Customer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name + str(self.time_created)


class OrderRespondStatus(models.Model):
    name = models.CharField(max_length=256, blank=False)
    value = models.CharField(max_length=256, blank=False)

    @staticmethod
    def getDafaultValue():
        return OrderRespondStatus.objects.get(value="new")

    @staticmethod
    def getRejectedValue():
        return OrderRespondStatus.objects.get(value="rejected")

    @staticmethod
    def getAcceptedValue():
        return OrderRespondStatus.objects.get(value="accepted")

    def __str__(self):
        return self.name


class OrderRespond(models.Model):
    order = models.ForeignKey(
        to=SimpleOrder, on_delete=models.CASCADE, null=False, blank=False)

    customer = models.ForeignKey(
        to=Customer, on_delete=models.CASCADE, null=False, blank=False)

    performer = models.ForeignKey(
        to=Performer, on_delete=models.CASCADE, null=False, blank=False)

    status = models.ForeignKey(
        to=OrderRespondStatus, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return str(self.order.id) + " " + str(self.customer.id) + " " + str(self.performer.id)
