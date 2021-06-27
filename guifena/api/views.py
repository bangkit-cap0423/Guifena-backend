from django.views import generic
from pyfcm.fcm import FCMNotification
from .serializers import IncidentSerializer, SensorSerializers
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
# Create your views here.
from .models import Sensors, Incidents, Token
import datetime
from django.utils import timezone
from django_q.tasks import async_task
import api.constanta as const
from rest_framework import status


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
            timestamp__range=(created_time, now)).order_by('-id')
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

# {"sensor_id": 1, "audio": "dasdadasdwasd"}


class ReceiveAudio(APIView):
    def post(self, request):
        data = request.data
        sensor_id = data['sensor_id']
        if 'audio' in data:
            audio = data['audio']
            time = timezone.now()
            async_task('api.tasks.printToConsole', audio, time, sensor_id)
        sensor = Sensors.objects.get(id=sensor_id)
        sensor.last_seen = timezone.now()
        sensor.save()
        return Response({'status': 'OK'})


class ChangeStatusIncident(APIView):
    def post(self, request):
        data = request.data
        incident_id = data['incident_id']
        status = data['status']
        try:
            incident = Incidents.objects.get(id=incident_id)
            incident.status = status
            incident.save()
            return Response({'status': 'OK'})
        except:
            return Response({'status': 'FAILED'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReceiveToken(APIView):
    def post(self, request):
        data = request.data
        token = data['token']
        check_token = Token.objects.filter(token=token).count()
        if check_token > 0:
            return Response({'status': 'OK'})
        Token.objects.create(token=token)
        return Response({'status': 'OK'})


class AddSensor(APIView):
    def post(self, request):
        data = request.data
        nama = data['nama']
        location = data['location']
        # check if given name is already on db
        sensor = Sensors.objects.filter(nama=nama).first()
        if sensor:
            # name is already on db
            sensor.location = location
            sensor.save()
            payload = {"status": "OK", "sensor_id": sensor.id}
            return Response(payload)
        else:
            sensor = Sensors(nama=nama, location=location,
                             status=0, last_seen=timezone.now())
            sensor.save()
            payload = {"status": "OK", "sensor_id": sensor.id}
            return Response(payload)


def sendNotification():
    api_key = 'AAAAej261Qg:APA91bFNLBEeIl_ZPTi98ct_fudgnUDsVEE8Xd7mB9azDSGk5Hu8xJWc8AO6AvNohdySg9hJe7uSdyTwUsoehGKzYbr8JOMZmoVv0Vm3SWmiqlEhy0iFOqB1wMGEgzAMRseJNokpFIPF'
    tokens = []
    query_token = Token.objects.all()
    for query in query_token:
        tokens.append(query.token)
    push_service = FCMNotification(api_key=api_key)
    data_message = {
        "raisa": 'ok',

    }
    push_service.notify_multiple_devices(
        registration_ids=tokens, data_message=data_message)

        
class sendNotificationDummy(APIView):
    def get(self, request):
        time = timezone.now()
        sensor = Sensors.objects.get(id=1)
        Incidents.objects.create(
            sensor=sensor,
            status=1,
            timestamp=time
        )
        sendNotification()
