# serializers.py
from rest_framework import serializers
from .models import Location, ClusteredIncidentsView

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class ClusteredIncidentsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClusteredIncidentsView
        fields = '__all__'
