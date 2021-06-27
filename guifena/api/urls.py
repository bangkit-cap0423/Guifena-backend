from django.urls import path
#from rest_framework.authtoken import views
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.GetCount.as_view()),
    path('sensors/', views.ListSensors.as_view()),
    path('sensors/<int:id>/', views.GetSensorDetail.as_view()),
    path('incidents/', views.ListIncidents.as_view()),
    path('incidents/recents/', views.ListRecentIncidents.as_view()),
    path('incidents/<int:id>', views.GetIncidentDetail.as_view()),
    path('incidents/changestatus/', views.ChangeStatusIncident.as_view()),
    path('sensors/upload/', views.ReceiveAudio.as_view()),
    path('sensors/add/', views.AddSensor.as_view()),
    path('token/', views.ReceiveToken.as_view()),
    path('tasya/', views.sendNotificationDummy.as_view()),
]
