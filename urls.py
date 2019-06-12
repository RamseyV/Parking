from django.urls import path, include
from . import views
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

app_name = "parking"

urlpatterns = [
    path('', views.parking, name='parking'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

