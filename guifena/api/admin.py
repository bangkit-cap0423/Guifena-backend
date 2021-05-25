from django.contrib import admin
from .models import Sensors, Incidents, Token
# Register your models here.

admin.site.register(Sensors)
admin.site.register(Incidents)
admin.site.register(Token)
