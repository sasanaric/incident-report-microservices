from rest_framework import serializers
from .models import *

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'
class IncidentAnalysisTypesSerializer(serializers.Serializer):
    group_type_id = serializers.IntegerField()
    total = serializers.IntegerField()

class IncidentAnalysisMonthsSerializer(serializers.Serializer):
    month = serializers.CharField()
    total = serializers.IntegerField()
class IncidentAnalysisDaysSerializer(serializers.Serializer):
    day = serializers.CharField()
    total = serializers.IntegerField()


