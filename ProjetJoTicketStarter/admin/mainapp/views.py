from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from .models import Stadium
from .serializers import StadiumSerializer

@api_view(['GET'])
def stadiums(request):
    stadiums_list = Stadium.objects.all()
    serializer = StadiumSerializer(stadiums_list, many=True)
    return Response(serializer.data)
