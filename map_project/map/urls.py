from django.urls import path
from .views import *

urlpatterns = [
    path('locations/', LocationList.as_view(), name='location-list'),
    path('locations/<int:pk>/', LocationDetail.as_view(), name='location-detail'),
        path('locations/distance/<slug:dist>/<path:coordinates>/', LocationsWithinDistance.as_view(), name='location-distance'),

]