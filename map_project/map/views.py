# views.py

from rest_framework import generics
from .models import Location
from .serializers import LocationSerializer
from rest_framework.views import APIView
from django.contrib.gis.geos import Point
from django.db import connection
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from .serializers import LocationSerializer
from django.http import HttpResponse

class LocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationsWithinDistance(generics.ListCreateAPIView):
    serializer_class = LocationSerializer

    def get_queryset(self):
        lat, lon = map(float, self.kwargs["coordinates"].split(","))
        dist = float(self.kwargs["dist"])

        target_location = GEOSGeometry(f"POINT({lon} {lat})", srid=4326)

        queryset = Location.objects.annotate(
            distance=Distance("coordinates", target_location)
        ).filter(distance__lte=D(km=dist))

        return queryset

