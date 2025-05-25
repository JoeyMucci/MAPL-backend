from django.utils import timezone
from .models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import BoutSerializer
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_todays_bouts(request):
    today = timezone.now().date()
    bouts = Bout.objects.filter(time__date=today)

    try:
        serializer = BoutSerializer(bouts, many=True)
        serialized_bouts = serializer.data
    except Exception as e:
        return Response(
            {'error': f'Serializer error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response(serialized_bouts, status=status.HTTP_200_OK)






