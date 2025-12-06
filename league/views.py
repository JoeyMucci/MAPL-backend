from .models import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.db.models import Avg, Min, Max, Count, F, Q
import re
import calendar


BOUTS_PER_SEASON = 24
DAYS_PER_MONTH = 25
divisions = ["Master", "All-Star", "Professional", "Learner"]

def camelcase_to_words(s):
    words = re.sub('([a-z])([A-Z])', r'\1 \2', s)
    return words.title()

def get_last_complete_date():
    last_bout = Bout.objects.filter(away_roll__isnull=False).order_by('time').reverse()[0]
    day = last_bout.day
    month = last_bout.month
    year = last_bout.year

    if not last_bout.last_in_day:
        day -= 1
        if day == 0:
            month -= 1
            day = DAYS_PER_MONTH
            if month == 0:
                month = 12
                year -= 1

    return year, month, day

def get_last_complete_month():
    year, month, day = get_last_complete_date()

    if day != DAYS_PER_MONTH:
        month -= 1
        if month == 0:
            month = 12
            year -= 1
    
    return year, month

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
            {'error': f'Serializing error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response(serialized_pebbler, status=status.HTTP_200_OK)

# Return the bouts for the requested day
@api_view(['GET'])
def get_bouts(request, month, day, year):
    bouts = Bout.objects.filter(month=month, day=day, year=year)
    bouts_sorted = bouts.order_by('time')

    bout_info = {}

    try:
        for division in divisions:
            division_bouts = bouts_sorted.filter(division=division)
            serializer = BoutSmall(division_bouts, many=True)
            serialized_bouts = serializer.data
            bout_info[division] = serialized_bouts
    except Exception as e:
        return Response(
            {'error': f'Serializing error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response({"bout_info": bout_info}, status=status.HTTP_200_OK)

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
            {'error': f'Serializing error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response({"bouts" : serializer.data}, status=status.HTTP_200_OK)


def get_rivalry_bouts_helper(pebblerOne, pebblerTwo, includeBouts):
    pebbler_one_name = camelcase_to_words(pebblerOne)
    pebbler_two_name = camelcase_to_words(pebblerTwo)

    try:
        pebbler_one = Pebbler.objects.get(name=pebbler_one_name)
        pebbler_two = Pebbler.objects.get(name=pebbler_two_name)
    except Pebbler.DoesNotExist:
        return Response(
            {'error': 'At least one pebbler not found'}, 
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

    if includeBouts:
        try: 
            serializer = BoutSmall(all_bouts_sorted, many=True)
        except Exception as e:
            return Response(
                {'error': f'Serializing error: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return {
            "division_pebbles" : division_pebbles,
            "division_wtl" : division_wtl,
            "bouts" : serializer.data,
        }
    else:
        return {
            "division_pebbles" : division_pebbles,
            "division_wtl" : division_wtl,
        }

# Return the bouts between pebblerOne and pebblerTwo
@api_view(['GET'])
def get_rivalry_bouts(request, pebblerOne, pebblerTwo):
    return Response(get_rivalry_bouts_helper(pebblerOne, pebblerTwo, includeBouts=True), status=status.HTTP_200_OK)

# Return the bout with matching id
@api_view(['GET'])
def get_bout_by_id(request, id):
    bout = get_object_or_404(Bout, pk=id)
    try:
        serializer = BoutFull(bout)
    except Exception as e:
        return Response(
            {'error': f'Serializing error: {str(e)}'}, 
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
            {'error': f'Serializing error: {str(e)}'}, 
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
            {'error': f'Serializing error: {str(e)}'}, 
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

# Return recent winners for the past four months
@api_view(['GET'])
def get_recent_winners(request):
    year, month = get_last_complete_month()

    count = 4
    recent_winning_performances = Performance.objects.filter(
        rank=1,
        year=year,
        month__gte=month - (count - 1), 
        month__lte=month
    ) | Performance.objects.filter(
        rank=1,
        year=year - 1,
        month__gte=month - (count - 1) + 12, 
    )

    pebblers = [-1 for _ in range(len(recent_winning_performances))]

    for perf in recent_winning_performances:
        months_old = (year - perf.year) * 12 + (month - perf.month)
        idx = months_old * len(divisions) + divisions.index(perf.division)
        pebblers[idx] = perf.pebbler

    try:
        serializer = PebblerPersonal(pebblers, many=True)
    except Exception as e:
        return Response(
            {'error': f'Serializing error: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    month = month 
    year = year
    for i in range(len(serializer.data)):
        if i > 0 and i % 4 == 0:
            month -= 1
            if month == 0:
                month = 12
                year -= 1

        month_name = calendar.month_abbr[month]
        serializer.data[i]["description"] = divisions[i % 4] + f" {month_name} {year}"

    return Response(serializer.data, status=status.HTTP_200_OK)

# Return top 5 and bottom five pebblers in each division
@api_view(['GET'])
def get_ranking_bookends(request):
    data = {division : {
        "leaders" : [-1, -1, -1, -1, -1],
        "trailers" : [-1, -1, -1, -1, -1],
    } for division in divisions}

    for pebbler in Pebbler.objects.all():
        if pebbler.current_rank <= 5:
            data[pebbler.current_division]["leaders"][pebbler.current_rank - 1] = pebbler
        elif pebbler.current_rank >= 21:
            data[pebbler.current_division]["trailers"][pebbler.current_rank - 21] = pebbler

    try:
        for division in data:
            for classification in data[division]:
                serializer = PebblerPersonal(data[division][classification], many=True)
                data[division][classification] = serializer.data
    except Exception as e:
        return Response(
            {'error': f'Serializing error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    for division in data:
        for classification in data[division]:
            for i in range(len(data[division][classification])):
                data[division][classification][i]["description"] = (
                    division + " Rank: " + str(i + 1 + (20 if classification == "trailers" else 0))
                )

    flat_data = {
        "leaders": [],
        "trailers": [],
    }

    for classification in flat_data:
        for division in divisions:
            flat_data[classification].extend(data[division][classification])
    
    return Response(flat_data, status=status.HTTP_200_OK)


# Return top 5 ytd pebblers, and top quirk activators and ability
# triggers by each quirk and ability
@api_view(['GET'])
def get_ytd_stats(request):
    listLen = 5
    pebbleList = [-1, -1, -1, -1, -1]
    pebbleStrs = ["", "", "", "", ""]
    qpList = [-1, -1, -1, -1, -1]
    qpStrs = ["", "", "", "", ""]
    atList = [-1, -1, -1, -1, -1]
    atStrs = ["", "", "", "", ""]

    qMap = {
        "Pity Pebble": 0,
        "Proud Pebble": 1,
        "Oddball": 2,
        "Even Temper": 3,
        "Untouchable": 4,
    }

    aMap = {
        "Miracle": 0,
        "Lucky Seven": 1,
        "Generosity": 2,
        "Will to Win": 3,
        "Tip the Scales": 4,
    }

    if len(Pebbler.objects.all()) == 0:
        return Response(
            {'error': 'Pebblers not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    for pebbler in Pebbler.objects.all().order_by('?'):
        pebbleIndex = 4
        while (
            pebbleIndex >= 0 and 
            (pebbleList[pebbleIndex] == -1 or 
            pebbleList[pebbleIndex].ytd_pebbles < pebbler.ytd_pebbles)
        ):
            pebbleIndex -= 1

        pebbleList.insert(pebbleIndex + 1, pebbler)
        pebbleStrs.insert(pebbleIndex + 1, str(pebbler.ytd_pebbles))
        pebbleList.pop()
        pebbleStrs.pop()

        qIndex = qMap[pebbler.quirk]
        if qpList[qIndex] == -1 or qpList[qIndex].ytd_qp < pebbler.ytd_qp:
            qpList[qIndex] = pebbler
            qpStrs[qIndex] = pebbler.quirk + " - " + str(pebbler.ytd_qp)

        aIndex = aMap[pebbler.ability]
        if atList[aIndex] == -1 or atList[aIndex].ytd_at < pebbler.ytd_at:
            atList[aIndex] = pebbler
            atStrs[aIndex] = pebbler.ability + " - " + str(pebbler.ytd_at)

    try:
        pebbles = PebblerPersonal(pebbleList, many=True)
        quirks = PebblerPersonal(qpList, many=True)
        abilities = PebblerPersonal(atList, many=True)
    except Exception as e:
        return Response(
            {'error': f'Serializing error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    for i in range(listLen):
        pebbles.data[i]["description"] = pebbleStrs[i]
        quirks.data[i]["description"] = qpStrs[i]
        abilities.data[i]["description"] = atStrs[i]
    
    return Response({"pebbles": pebbles.data, "quirks": quirks.data, "abilities": abilities.data}, status=status.HTTP_200_OK)


# Return the pebbler with the greatest ranking change in each division
# Tiebreaker is higher rank (i.e. 15->10 would take precedence over 20->15)
@api_view(['GET'])
def get_hot_pebblers(request):
    year, month, day = get_last_complete_date()
    performances = Performance.objects.filter(month=month, year=year)
    
    if len(performances) == 0:
        return Response({}, status=status.HTTP_200_OK)
    
    try:
        performance_info = {}
        for division in divisions:
            hot_perf = performances.filter(division=division).order_by(
                F('rank') - F('previous_rank'),
                'rank'
            ).first()

            hot_bouts = Bout.objects.filter(month=month, year=year, day=day).filter(
                Q(away=hot_perf.pebbler) | Q(home=hot_perf.pebbler))
            
            if len(hot_bouts) == 1:
                hot_bout = hot_bouts[0]
                gain = hot_bout.away_score if hot_bout.away == hot_perf.pebbler else hot_bout.home_score
                hot_pebbler = [hot_perf.pebbler]
                serializer = PebblerPersonal(hot_pebbler, many=True)
                serializer.data[0]["description"] = f"{hot_perf.pebbles - gain}UP{hot_perf.pebbles} {hot_perf.previous_rank}UP{hot_perf.rank}"
                performance_info[division] = serializer.data
    except Exception as e:
        return Response(
            {'error': f'Serializing error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    date = {}
    date["year"] = year
    date["month"] = month
    date["day"] = day
    
    full_data = {}
    full_data["performance_info"] = performance_info
    full_data["date"] = date
    
    return Response(full_data, status=status.HTTP_200_OK)

# Return the five most recent bouts with an ability trigger
@api_view(['GET'])
def get_hot_bouts(request):
    hot_bouts = Bout.objects.filter(Q(away_ability=True) | Q(home_ability=True) | (Q(away_quirk=True) & Q(home_quirk=True))).order_by('time').reverse()[:5]

    try:
        serializer = BoutSmall(hot_bouts, many=True)
    except Exception as e:
        return Response(
            {'error': f'Serializing error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response(serializer.data, status=status.HTTP_200_OK)


# Return rivalry information for the next 5 bouts
@api_view(['GET'])
def get_hot_rivalries(request):
    hot_bouts = Bout.objects.filter(away_roll__isnull=True).order_by('time')[:5]

    rivalry_info = []

    for hot_bout in hot_bouts:
        rivalry_info.append({
            'one': hot_bout.away.name,
            'two': hot_bout.home.name,
            'data': get_rivalry_bouts_helper(hot_bout.away.name, hot_bout.home.name, includeBouts=False),
        })

    return Response(rivalry_info, status=status.HTTP_200_OK)
