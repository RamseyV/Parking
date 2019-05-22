from django.urls import path, include
from . import views
from django.conf.urls import url


app_name = "parking"

urlpatterns = [
    path('', views.parking, name='parking'),
    url(r'^api/occupied_history_json', views.occupied_history_json, name='occupied_history_json'),
]

