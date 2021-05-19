from rest_framework import serializers
from .models import Sensors, Incidents


class SensorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sensors
        fields = '__all__'


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incidents
        fields = '__all__'
