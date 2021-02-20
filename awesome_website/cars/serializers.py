'''
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
'''

from rest_framework import serializers

from .models import Car, Service


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ['id', 'brand', 'model', 'year', 'vin']


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ['id', 'place', 'repair', 'cost', 'date', 'car_id']


        #place = models.CharField(blank=True, null=True, max_length=200)
        #repair = models.TextField(blank=True, null=True)
        #cost = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)
        #date = models.DateField(blank=True, default='', null=True)
        #car = models.ForeignKey(Car, on_delete=models.CASCADE)