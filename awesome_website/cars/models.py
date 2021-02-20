from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=200, default="-")
    model = models.CharField(max_length=200, default="-")
    year = models.IntegerField(default=0, null=True)
    vin = models.CharField(max_length=40, null=True)
    user_id = models.IntegerField(default=0)
    

class Service(models.Model):
    place = models.CharField(blank=True, null=True, max_length=200)
    repair = models.TextField(blank=True, null=True)
    cost = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)
    date = models.DateField(blank=True, default='', null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
