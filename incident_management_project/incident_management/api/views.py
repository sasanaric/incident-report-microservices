from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from ..models import Incident
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):

    routes=[
        '/api/token',
        '/api/token/refresh',
    ]

    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def restrictedView(request):
    return Response({"message": "This is a restricted view. Only authenticated users can access."})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approveIncident(request):
    id = request.data.get('id')
    try:
        incident = Incident.objects.get(id=id)
    except Incident.DoesNotExist:
        raise Http404("Incident does not exist")

    incident.approved = True
    incident.save()
    return Response({"message": "Incident status updated."})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteIncident(request, id, *args, **kwargs):
    try:
        incident = Incident.objects.get(id=id)
        incident.delete()
        return Response({"message": "Incident deleted."})
    except Incident.DoesNotExist:
        raise Http404("Incident does not exist")
