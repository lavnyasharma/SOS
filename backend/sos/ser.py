from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password

from rest_framework.exceptions import APIException, NotFound

class serrr(serializers.ModelSerializer):

    class Meta:
        model = guest_sos
        fields = ('pno', 'time', 'status', 'long', 'lat', 'pin', 'ip', 'token')
