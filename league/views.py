from django.utils import timezone
from .models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.decorators import api_view

# Return the bouts for today, or the first day with bouts in up to the next 10 days
@api_view(['GET'])
def get_todays_bouts(request):
    today = timezone.now().date()
    bouts = Bout.objects.filter(time__date=today)
    attempts = 0

    while bouts.count() == 0 and attempts < 10:
        today += timezone.timedelta(days=1)
        bouts = Bout.objects.filter(time__date=today)
        attempts += 1

    day = today.day
    month = today.month

    try:
        serializer = BoutPreview(bouts, many=True)
        serialized_bouts = serializer.data
    except Exception as e:
        return Response(
            {'error': f'Serializer error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response({"day" : day, "month": month, "bout_info": serialized_bouts}, status=status.HTTP_200_OK)






