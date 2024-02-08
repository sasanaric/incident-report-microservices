from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics,status
import json
from incident_management.rabbitmq import RabbitMQSender
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import Q,Count, Func
from django.db.models.functions import Coalesce,TruncMonth,TruncDay



def send_message_to_rabbitmq(request,body):
    sender = RabbitMQSender()
    sender.send_message(queue_name='incident_deletion', message=json.dumps(body))
    sender.close_connection()
    return HttpResponse('Message sent to RabbitMQ.')
    
class IncidentList(generics.ListCreateAPIView):
    queryset = Incident.objects.all().order_by('id');
    serializer_class = IncidentSerializer

class ApprovedIncidentList(generics.ListCreateAPIView):
    queryset = Incident.objects.all().filter(approved = True)
    serializer_class = IncidentSerializer

class NotApprovedIncidentList(generics.ListCreateAPIView):
    queryset = Incident.objects.all().filter(approved = False)
    serializer_class = IncidentSerializer

class IncidentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

class AllTypesList(generics.ListCreateAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class TypeList(generics.ListCreateAPIView):
    queryset = Type.objects.all().filter(parent__isnull=True)
    serializer_class = TypeSerializer

class SubTypeList(generics.ListCreateAPIView):
    queryset = Type.objects.all().filter(parent__isnull=False)
    serializer_class = TypeSerializer

class TypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

class IncidentListByLocations(generics.ListCreateAPIView):
    serializer_class = IncidentSerializer

    def post(self, request, *args, **kwargs):
        
        location_ids = request.data.get('location_ids', [])

        if not location_ids:
            return Response({"error": "location_ids must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Incident.objects.filter(location_id__in=location_ids)
        print(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class IncidentListFilter(generics.ListAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['time', 'type', 'approved']

    def post(self, request, *args, **kwargs):
        days = request.data.get('days')
        incident_type = request.data.get('type')
        approved = request.data.get('approved')
        location_ids = request.data.get('location_ids',[])
        type_ids = Type.objects.filter(Q(id=incident_type) | Q(parent=incident_type))

        queryset = self.get_queryset()
        if days:
            within_days = timezone.now() - timezone.timedelta(days=days)
            queryset = queryset.filter(time__gte=within_days)
        if incident_type:
            queryset = queryset.filter(type__in=type_ids)
        if approved is not None:
            queryset = queryset.filter(approved=approved)
        if location_ids:
            queryset = queryset.filter(location_id__in=location_ids)
        print(queryset)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class GroupedIncidentsView(APIView):
    def get(self, request, *args, **kwargs):
        incidents = Incident.objects.all()

        descriptions = [incident.description for incident in incidents]

        descriptions = [desc.lower() if desc else '' for desc in descriptions]

        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(descriptions)

        kmeans = KMeans(n_clusters=8)  
        clusters = kmeans.fit_predict(X)

        for incident, cluster in zip(incidents, clusters):
            incident.cluster_label = cluster
            incident.save()

        grouped_incidents = {}
        for incident in incidents:
            cluster = int(incident.cluster_label)
            if cluster not in grouped_incidents:
                grouped_incidents[cluster] = {'cluster_label': cluster, 'incidents': []}
            serializer = IncidentSerializer(incident)
            grouped_incidents[cluster]['incidents'].append(serializer.data)

        return JsonResponse(list(grouped_incidents.values()), safe=False)

class IncidentAnalysisTypesView(generics.ListAPIView):
    serializer_class = IncidentAnalysisTypesSerializer

    def get(self, request, *args, **kwargs):
        queryset = (
            Incident.objects
            .annotate(
                group_type_id=Coalesce('type__parent', 'type__id', output_field=models.IntegerField()),
            )
            .values('group_type_id')
            .annotate(total=Count('group_type_id'))
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class IncidentAnalysisMonthsView(generics.ListAPIView):
    serializer_class = IncidentAnalysisMonthsSerializer

    def get(self, request, *args, **kwargs):
        twelve_months_ago = datetime.now() - timedelta(days=365)

        queryset = (
            Incident.objects
            .filter(time__gte=twelve_months_ago)
            .values(month=TruncMonth('time'))
            .order_by('month')
            .reverse()
            .annotate(total=Count('id'))
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class IncidentAnalysisDaysView(generics.ListAPIView):
    serializer_class = IncidentAnalysisDaysSerializer

    def get(self, request, *args, **kwargs):
        seven_days_ago = datetime.now() - timedelta(days=7)

        queryset = (
            Incident.objects
            .filter(time__gte=seven_days_ago)
            .values(day=TruncDay('time'))
            .annotate(total=Count('id'))
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


