from django.db.models import fields
from doctors.models import doc_specialization, doctor, hospital, office, specialization
from rest_framework.serializers import ModelSerializer

from user.models import user


class docser(ModelSerializer):
    class Meta:
        model = doctor
        fields = ('registration_number', "professional_statement",
                  'slug', "practicing_from")


class SpecializationSer(ModelSerializer):
    class Meta:
        model = specialization
        fields = ('SPEID', 'name')


class doc_specializationSer(ModelSerializer):
    class Meta:
        model = doc_specialization
        fields = ('SPEID', 'DOCID')


class HospitalSer(ModelSerializer):
    class Meta:
        model = hospital
        fields = '__all__'


class OfficeSer(ModelSerializer):
    class Meta:
        model = office
        fields = '__all__'


class usseSer(ModelSerializer):
    class Meta:
        model = user
        fields = ('first_name', "last_name",)
