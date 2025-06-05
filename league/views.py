from django.utils import timezone
from .models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.decorators import api_view
import re
from datetime import date

BOUTS_PER_SEASON = 24
divisions = ["Master", "All-Star", "Professional", "Learner"]

def camelcase_to_words(s):
    words = re.sub('([a-z])([A-Z])', r'\1 \2', s)
    return words.title()


def get_pebbler_info(pebblerName, PebblerSerializer):
    pebbler_name = camelcase_to_words(pebblerName)

    try:
        pebbler = Pebbler.objects.get(name=pebbler_name)
    except Pebbler.DoesNotExist:
        return Response(
            {'error': 'Pebbler not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        serializer = PebblerSerializer(pebbler)
        serialized_pebbler = serializer.data
    except Exception as e:
        return Response(
            {'error': f'Serializer error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response(serialized_pebbler, status=status.HTTP_200_OK)
# Return the request pebbler's basic information
@api_view(['GET'])
def get_pebbler_basic_info(request, pebblerName):
    return get_pebbler_info(pebblerName, PebblerBasic)

# Return the request pebbler's personal information
@api_view(['GET'])
def get_pebbler_personal_info(request, pebblerName):
    return get_pebbler_info(pebblerName, PebblerPersonal)

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

    if bouts.count() == 0:
        return Response(
            {'error': f'No bouts to display'}, 
            status=status.HTTP_404_NOT_FOUND
        )

    day = today.day
    month = today.month
    bout_info = {}

    try:
        for division in divisions:
            division_bouts = bouts.filter(division=division)
            serializer = BoutSmall(division_bouts, many=True)
            serialized_bouts = serializer.data
            bout_info[division] = serialized_bouts
    except Exception as e:
        return Response(
            {'error': f'Serializer error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response({"day" : day, "month": month, "bout_info": bout_info}, status=status.HTTP_200_OK)

# Return the bouts belonging to the pebbler from the last 3 months including this one
@api_view(['GET'])
def get_pebbler_bouts(request, pebblerName):
    pebbler_name = camelcase_to_words(pebblerName)

    try:
        pebbler = Pebbler.objects.get(name=pebbler_name)
    except Pebbler.DoesNotExist:
        return Response(
            {'error': 'Pebbler not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    today = timezone.now().date()
    year = today.year
    month = today.month - 2
    if month <= 0:
        month += 12
        year -= 1
    first_date = date(year, month, 1)
    
    home_bouts = pebbler.home_bouts.filter(home_roll__isnull=False, time__date__gte=first_date) # Using related name
    away_bouts = pebbler.away_bouts.filter(away_roll__isnull=False, time__date__gte=first_date) # Using related name
    all_bouts = home_bouts | away_bouts
    sorted_bouts = sorted(all_bouts, key=lambda bout: bout.time, reverse=True)

    try:
        serializer = BoutSmall(sorted_bouts, many=True)
    except Exception as e:
        return Response(
            {'error': f'Serializer error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response(serializer.data, status=status.HTTP_200_OK)

# Get the rankings for the requested month and year broken out by division
@api_view(['GET'])
def get_ranked_performances(request, month, year):
    performances = Performance.objects.filter(month=month, year=year)

    if performances.count() == 0:
        return Response(
            {'error': f'No performances to display'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    performance_info = {}
    
    try:
        for division in divisions:
            division_performances = performances.filter(division=division).order_by(
                '-pebbles', '-qp', '-wins', '-ties', '-pd', '-pf', 'tiebreaker'
            )
            serializer = PerformanceMain(division_performances, many=True)
            serialized_performances = serializer.data
            performance_info[division] = serialized_performances
    except Exception as e:
        return Response(
            {'error': f'Serializer error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response(performance_info, status=status.HTTP_200_OK)

# Performances from last 12/13 months sorted from earliest to latest
@api_view(['GET'])
def get_performance_history(request, pebblerName):
    pebbler_name = camelcase_to_words(pebblerName)

    try:
        pebbler = Pebbler.objects.get(name=pebbler_name)
    except Pebbler.DoesNotExist:
        return Response(
            {'error': 'Pebbler not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

    today = timezone.now().date()
    year = today.year - 1
    month = today.month

    performances_1 = Performance.objects.filter(pebbler__name=pebbler_name, played=BOUTS_PER_SEASON, year__gt=year)
    performances_2 = Performance.objects.filter(pebbler__name=pebbler_name, played=BOUTS_PER_SEASON, year=year, month__gte=month)
    performances = performances_1 | performances_2

    sorted_performances = sorted(performances, key=lambda perf: perf.year + perf.month / 15)

    try:
        serializer = PebblerDivisionSummary(pebbler)
        serialized_pebbler = serializer.data
        serializer = PerformanceSummary(sorted_performances, many=True)
        serialized_performances = serializer.data
    except Exception as e:
        return Response(
            {'error': f'Serializer error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response({"distribution": serialized_pebbler, "performances": serialized_performances}, status=status.HTTP_200_OK)
    

    
    


