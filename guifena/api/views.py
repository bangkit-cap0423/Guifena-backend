from django.views import generic
from .serializers import IncidentSerializer, SensorSerializers
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
# Create your views here.
from .models import Sensors, Incidents
import datetime
from django.utils import timezone
from django_q.tasks import async_task
import api.constanta as const


class index(APIView):
    def get(self, request):
        return Response({"status": "guifena"})


class ListSensors(generics.ListAPIView):
    serializer_class = SensorSerializers

    def get_queryset(self):
        query = Sensors.objects.all().order_by('id')
        return query


class GetSensorDetail(APIView):
    def get(self, request, id):
        sensor = Sensors.objects.get(id=id)
        data = SensorSerializers(sensor)
        return Response(data.data)


class ListIncidents(generics.ListAPIView):
    serializer_class = IncidentSerializer

    def get_queryset(self):
        query = Incidents.objects.all().order_by('-id')
        return query


class ListRecentIncidents(generics.ListAPIView):
    serializer_class = IncidentSerializer

    def get_queryset(self):
        now = datetime.datetime.now()
        created_time = now - datetime.timedelta(minutes=60)
        incidents = Incidents.objects.filter(
            timestamp__range=(created_time, now))
        return incidents


class GetIncidentDetail(APIView):
    def get(self, request, id):
        incident = Incidents.objects.get(id=id)
        data = IncidentSerializer(incident)
        return Response(data.data)


class GetCount(APIView):
    def get(self, request):
        now = datetime.datetime.now()
        created_time = now - datetime.timedelta(minutes=10)
        sensors_count = Sensors.objects.filter(
            last_seen__range=(created_time, now)).count()
        incidents_count = Incidents.objects.filter(
            timestamp__range=(created_time, now)).count()
        incidents_ongoing = Incidents.objects.filter(
            status__lt=const.INCIDENTS_RESOLVED).count()
        payload = {
            "sensors_count": sensors_count,
            "incidents_count": incidents_count,
            "all_good": incidents_ongoing == 0
        }
        return Response(payload)

#{"sensor_id": 1, "audio": "dasdadasdwasd"}


class ReceiveAudio(APIView):
    def post(self, request):
        data = request.data
        sensor_id = data['sensor_id']
        #audio = data['audio']
        # send audio to background task
        # TODO: CHANGE THIS WITH THE REAL ML
        async_task('api.tasks.printToConsole', "farin")
        sensor = Sensors.objects.get(id=sensor_id)
        sensor.last_seen = timezone.now()
        sensor.save()
        return Response({'status': 'OK'})
