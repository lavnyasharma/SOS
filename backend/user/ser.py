from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Address, PhoneNumber, Pincode, user
from django.contrib.auth.password_validation import validate_password

from rest_framework.exceptions import APIException, NotFound


class UpdateSer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,  validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = user
        fields = ('password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'password': {'required': False},
            'password2': {'required': False}
        }

    def validate(self, attrs):
        print('hello')
        if 'password' in attrs:
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError(
                    {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        try:
            userinstance = user.objects.fliter(
                UID='8e8da6f5-c844-478b-a221-f87d83c898a9'
            ).first()
            if 'password' in validated_data:
                userinstance.set_password(validated_data['password'])
            if 'first_name' in validated_data:
                userinstance.first_name = validated_data['first_name']
            if 'last_name' in validated_data:
                userinstance.last_name = validated_data['last_name']
            userinstance.save()
        except Exception as e:
            return APIException(NotFound)

        return user


class AddressSer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ('address_line_one', 'address_line_two',
                  'address_line_three', 'address_line_four', 'district', 'state', 'is_home', 'AID', 'PHID', 'PCID')
        extra_kwargs = {
            'AID': {'read_only': True},
            'PHID': {'read_only': True},
            'PCID': {'read_only': True}
        }


class PhoneSer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('PHID', 'phone_number')
        extra_kwargs = {
            'PHID': {'read_only': True},
        }


class PincodeSer(serializers.ModelSerializer):
    class Meta:
        model = Pincode
        fields = ('PCID', 'pincode_number')
        extra_kwargs = {
            'PCID': {'read_only': True},
        }


class UserProfileSer(serializers.ModelSerializer):

    class Meta:
        model = user
        fields = ['phone_number', 'first_name',
                  'last_name', 'email', 'gender', 'age', 'pin',  'address']
        
        
