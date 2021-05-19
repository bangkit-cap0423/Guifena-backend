from django.contrib import admin
from .models import Sensors, Incidents
# Register your models here.

admin.site.register(Sensors)
admin.site.register(Incidents)
