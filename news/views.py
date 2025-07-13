from league.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_news(request, month, day, year):
    bouts = Bout.objects.filter(month=month, day=day, year=year)

    serializer = BoutFull(bouts, many=True)

    return Response({
        "month": month, 
        "day": day, 
        "year": year, 
        "bouts": serializer.data}, 
        status=status.HTTP_200_OK
    )