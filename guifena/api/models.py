from django.db import models

# Create your models here.
#{"id": 1, "location": "1231231,131231", "status": 1, "last_seen": "2021-05-12T14:04:14+0000" }
class Sensors(models.Model):
    nama = models.CharField(max_length=40)
    location = models.TextField()
    status = models.PositiveIntegerField()
    last_seen = models.DateTimeField()


#{"id": 1, "sensor_id": 1, "sensor_name": "Titik 1",
#  "sensor_location": "1231231,131231", "timestamp": "2021-05-12T14:04:14+0000", "status": 1 }
class Incidents(models.Model):
    sensor = models.ForeignKey(Sensors, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.PositiveIntegerField()

