from .serializers import IncidentSerializer, SensorSerializers
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
# Create your views here.
from .models import Sensors, Incidents


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


class GetIncidentDetail(APIView):
    def get(self, request, id):
        incident = Incidents.objects.get(id=id)
        data = IncidentSerializer(incident)
        return Response(data.data)
