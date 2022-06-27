from pyexpat import model
from django.db import models

from user.models import Pincode

# Create your models here.


class guest_sos(models.Model):
    pno = models.CharField(max_length=150)
    time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=150, default='active')
    long = models.FloatField(default=0)
    lat = models.FloatField(default=0)
    pin = models.CharField(max_length=150, null=False)
    ip = models.CharField(max_length=150, default="")
    token = models.CharField(max_length=500, primary_key=True)


class update_quads(models.Model):
    token = models.CharField(max_length=500)
    long = models.FloatField(default=0)
    lat = models.FloatField(default=0)
    time = models.DateTimeField(auto_now=True)


class freeway(models.Model):
    pno = models.CharField(max_length=150)
    time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=150)
    long = models.FloatField(default=0)
    lat = models.FloatField(default=0)
    pin = models.CharField(max_length=150, null=False)
    ip = models.CharField(max_length=150, default="")
    token = models.CharField(max_length=500, primary_key=True)
