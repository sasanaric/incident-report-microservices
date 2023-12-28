# views.py

from rest_framework import generics
from .models import Location, ClusteredIncidentsView
from .serializers import LocationSerializer
from rest_framework.views import APIView
from django.contrib.gis.geos import Point
from django.db import connection
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from .serializers import LocationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ClusteredIncidentsViewSerializer
from django.db import connection
from django.http import JsonResponse

class LocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all().order_by('id')
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

def execute_sql_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

class ClusteredIncidentsViewList(APIView):
    def get(self, request, format=None):
        query = """
                    WITH ClusteredIncidents AS (
                        SELECT
                            id,
                            coordinates,
                            ST_DWithin(coordinates::geography, LAG(coordinates) OVER (ORDER BY coordinates), 5000) AS within_5km
                        FROM
                            map_location
                        WHERE
                            deleted = false
                        ORDER BY
                            coordinates DESC
                        LIMIT
                            100
                    )
                    SELECT
                        id,
                        ST_Y(coordinates) AS lat,
                        ST_X(coordinates) AS lon,
                        SUM(CASE WHEN within_5km THEN 1 ELSE 0 END) OVER (ORDER BY coordinates) AS cluster_size
                    FROM
                        ClusteredIncidents
                    WHERE
                        within_5km OR COALESCE(within_5km, false)
                    HAVING
                        SUM(CASE WHEN within_5km THEN 1 ELSE 0 END) > 10
                    ORDER BY
                        id;
                """
        results = execute_sql_query(query)

        return JsonResponse(results, safe=False);

class NewClusterView(APIView):
        def get(self, request, format=None):
            
            print("NEWCLUSTERVIEW")
            recent_locations = Location.objects.all().order_by('id')[:100]
            alarming_locations = []   
            for location in recent_locations:
                nearby_locations = (
                    Location.objects
                    .filter(coordinates__distance_lte=(location.coordinates, D(km=6)))
                    .exclude(id=location.id)
                )
                number_of_incidents = nearby_locations.count()
                if number_of_incidents > 9:
                    print(f"Alert: Frequent locations near {location.coordinates}")
                    location_data = {
                    'id': location.id,
                    'lat': location.coordinates.y,
                    'lon': location.coordinates.x, 
                    'locations': number_of_incidents
                }
                    alarming_locations.append(location_data)

            return JsonResponse(alarming_locations, safe=False)

