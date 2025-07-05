from .models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.db.models import Avg, Min, Max, Count, Sum, F
import re


BOUTS_PER_SEASON = 24
divisions = ["Master", "All-Star", "Professional", "Learner"]

def camelcase_to_words(s):
    words = re.sub('([a-z])([A-Z])', r'\1 \2', s)
    return words.title()


# Return the pebbler's basic information
@api_view(['GET'])
def get_pebbler_basic_info(request, pebblerName):
    return get_pebbler_info(pebblerName, PebblerBasic)

# Return the pebbler's personal information
@api_view(['GET'])
def get_pebbler_personal_info(request, pebblerName):
    return get_pebbler_info(pebblerName, PebblerPersonal)

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

# Return the bouts for the requested day
@api_view(['GET'])
def get_bouts(request, month, day, year):
    bouts = Bout.objects.filter(month=month, day=day, year=year)

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
    
    return Response({"month": month, "day" : day, "year": year, "bout_info": bout_info}, status=status.HTTP_200_OK)

# Return the bouts for the requested pebbler and month
@api_view(['GET'])
def get_pebbler_bouts(request, pebblerName, month, year):
    pebbler_name = camelcase_to_words(pebblerName)

    try:
        pebbler = Pebbler.objects.get(name=pebbler_name)
    except Pebbler.DoesNotExist:
        return Response(
            {'error': 'Pebbler not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Using related name
    home_bouts = pebbler.home_bouts.filter(home_roll__isnull=False, month=month, year=year) 
    away_bouts = pebbler.away_bouts.filter(away_roll__isnull=False, month=month, year=year) 
    all_bouts = (home_bouts | away_bouts)
    all_bouts_sorted = all_bouts.order_by('time').reverse()

    try: 
        serializer = BoutSmall(all_bouts_sorted, many=True)
    except Exception as e:
        return Response(
            {'error': f'Serializer error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response({"bouts" : serializer.data}, status=status.HTTP_200_OK)

# Return the bouts between pebblerOne and pebblerTwo
@api_view(['GET'])
def get_rivalry_bouts(request, pebblerOne, pebblerTwo):
    pebbler_one_name = camelcase_to_words(pebblerOne)
    pebbler_two_name = camelcase_to_words(pebblerTwo)

    try:
        pebbler_one = Pebbler.objects.get(name=pebbler_one_name)
        pebbler_two = Pebbler.objects.get(name=pebbler_two_name)
    except Pebbler.DoesNotExist:
        return Response(
            {'error': 'One pebbler not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Using related name
    home_bouts = pebbler_one.home_bouts.filter(home_roll__isnull=False, away=pebbler_two)
    away_bouts = pebbler_one.away_bouts.filter(away_roll__isnull=False, home=pebbler_two)
    all_bouts = (home_bouts | away_bouts)
    all_bouts_sorted = all_bouts.order_by('time').reverse()

    division_pebbles = {division : {"one_score" : 0, "two_score" : 0} for division in divisions}
    division_wtl = {division: {"one_wins": 0, "two_wins": 0, "ties": 0} for division in divisions}

    for bout in home_bouts:
        division_pebbles[bout.division]["one_score"] += bout.home_score
        division_pebbles[bout.division]["two_score"] += bout.away_score
        if bout.home_roll_final > bout.away_roll_final:
            division_wtl[bout.division]["one_wins"] += 1
        elif bout.away_roll_final > bout.home_roll_final:
            division_wtl[bout.division]["two_wins"] += 1
        else:
            division_wtl[bout.division]["ties"] += 1

    for bout in away_bouts:
        division_pebbles[bout.division]["one_score"] += bout.away_score
        division_pebbles[bout.division]["two_score"] += bout.home_score
        if bout.away_roll_final > bout.home_roll_final:
            division_wtl[bout.division]["one_wins"] += 1
        elif bout.home_roll_final > bout.away_roll_final:
            division_wtl[bout.division]["two_wins"] += 1
        else:
            division_wtl[bout.division]["ties"] += 1

    try: 
        serializer = BoutSmall(all_bouts_sorted, many=True)
    except Exception as e:
        return Response(
            {'error': f'Serializer error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response({
        "division_pebbles" : division_pebbles,
        "division_wtl" : division_wtl,
        "bouts" : serializer.data,
        }, status=status.HTTP_200_OK)

# Return the bout with matching id
@api_view(['GET'])
def get_bout_by_id(request, id):
    bout = get_object_or_404(Bout, pk=id)
    try:
        serializer = BoutFull(bout)
    except Exception as e:
        return Response(
            {'error': f'Serializer error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response(serializer.data, status=status.HTTP_200_OK)


# Return the ranked performances for the requested month
@api_view(['GET'])
def get_ranked_performances(request, month, year):
    performances = Performance.objects.filter(month=month, year=year)

    try:
        performance_info = {}
        for division in divisions:
            sorted_perfs = performances.filter(division=division).order_by(
                '-pebbles',
                '-qp',
                '-wins',
                '-ties',
                '-pd',
                '-pf',
                'tiebreaker'
            )
            serializer = PerformanceMain(sorted_perfs, many=True)
            performance_info[division] = serializer.data
    except Exception as e:
        return Response(
            {'error': f'Serializer error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response({"rankings" : performance_info}, status=status.HTTP_200_OK)

# Return the performance history for the requested pebbler and month
@api_view(['GET'])
def get_performance_history(request, pebblerName, year):
    pebbler_name = camelcase_to_words(pebblerName)

    try:
        pebbler = Pebbler.objects.get(name=pebbler_name)
    except Pebbler.DoesNotExist:
        return Response(
            {'error': 'Pebbler not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Using related name, only take completed seasons
    performances = pebbler.performances.filter(played=BOUTS_PER_SEASON, year=year).order_by('-month') 

    try:
        serializer = PerformanceSummary(performances, many=True)
    except Exception as e:
        return Response(
            {'error': f'Serializer error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response({"performances": serializer.data}, status=status.HTTP_200_OK)

# Return aggregate data for all completed seasons for the requested pebbler
@api_view(['GET'])
def get_pebbler_aggregate(request, pebblerName):
    pebbler_name = camelcase_to_words(pebblerName)

    try:
        pebbler = Pebbler.objects.get(name=pebbler_name)
    except Pebbler.DoesNotExist:
        return Response(
            {'error': 'Pebbler not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Using related name, only take completed seasons
    data = pebbler.performances.filter(played=BOUTS_PER_SEASON).values('division').annotate(
        cnt=Count('id'),
        avg_rank=Avg('rank'), best_rank=Min('rank'), worst_rank=Max('rank'),
        avg_pebbles=Avg('pebbles'), best_pebbles=Max('pebbles'), worst_pebbles=Min('pebbles'),
        avg_wins=Avg('wins'), best_wins=Max('wins'), worst_wins=Min('wins'),
        avg_losses=Avg('losses'), best_losses=Min('losses'), worst_losses=Max('losses'),
        avg_pf=Avg('pf'), best_pf=Max('pf'), worst_pf=Min('pf'),
        avg_pa=Avg('pa'), best_pa=Min('pa'), worst_pa=Max('pa'),
        avg_pd=Avg('pd'), best_pd=Max('pd'), worst_pd=Min('pd'),
        avg_qp=Avg('qp'), best_qp=Max('qp'), worst_qp=Min('qp'),
        avg_at=Avg('at'), best_at=Max('at'), worst_at=Min('at'),
    )

    return Response(data, status=status.HTTP_200_OK)
    