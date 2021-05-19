from .serializers import SensorSerializers
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
