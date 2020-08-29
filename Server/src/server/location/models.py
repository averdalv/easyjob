from django.db import models


class City(models.Model):
    name = models.CharField(max_length=256, blank=False)
    value = models.CharField(max_length=256, blank=False)
    lat = models.FloatField()
    lon = models.FloatField()
    def __str__(self):
        return self.name

class Location(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    city = models.ForeignKey(to=City, on_delete=models.CASCADE)
    address = models.CharField(max_length=256, blank=False, null=True)


class OrderLocationType(models.Model):
    name = models.CharField(max_length=256, blank=False)
    value = models.CharField(max_length=256, blank=False)

    def __str__(self):
        return self.name

    @staticmethod
    def getRemote():
        return OrderLocationType.objects.get(value="in-remote")
