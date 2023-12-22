from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('incident_management.urls')),
    path('api/',include('incident_management.api.urls')),
]
