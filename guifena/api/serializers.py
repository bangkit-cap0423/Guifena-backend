from rest_framework import serializers
from .models import Sensors, Incidents


class SensorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sensors
        fields = '__all__'


class IncidentSerializer(serializers.ModelSerializer):
    sensor_id = serializers.ReadOnlyField(source='sensor.id')
    sensor_name = serializers.ReadOnlyField(source='sensor.nama')
    sensor_location = serializers.ReadOnlyField(source='sensor.location')

    class Meta:
        model = Incidents
        fields = ('sensor', 'sensor_id', 'sensor_name', 'sensor_location',
                  'timestamp', 'status', 'id')
