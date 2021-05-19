from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.

class index(APIView):
    def get(self, request):
        return Response({"status":"guifena"})