from django.urls import path
#from rest_framework.authtoken import views
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index.as_view()),
    path('sensors/', views.ListSensors.as_view()),
    path('sensors/<int:id>/', views.GetSensorDetail.as_view()),
    path('incidents/', views.ListIncidents.as_view()),
    path('incidents/<int:id>', views.GetIncidentDetail.as_view())
]
