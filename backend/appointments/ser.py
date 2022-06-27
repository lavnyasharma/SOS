from rest_framework.serializers import ModelSerializer
from .models import Appointment, batch


class AppointmentSerializer(ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class BatchSerializer(ModelSerializer):
    class Meta:
        model = batch
        fields = ('name', "date", 'BATCHID', 'status', 'active')
