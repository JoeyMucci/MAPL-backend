from news.models import *
from news.serializers import *
from rest_framework.response import Response
from rest_framework import status
import re
from rest_framework.decorators import api_view

def camelcase_to_words(s):
    words = re.sub('([a-z])([A-Z])', r'\1 \2', s)
    return words.title()

@api_view(['GET'])
def get_author(request, authorName):
    author_name = camelcase_to_words(authorName)

    try:
        author = Reporter.objects.get(name=author_name)
    except Pebbler.DoesNotExist:
        return Response(
            {'error': 'Pebbler not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        serializer = ReporterSerializer(author)
        serialized_author = serializer.data
    except Exception as e:
        return Response(
            {'error': f'Serializer error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response(serialized_author, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_news(request, month, year):
    reports = Report.objects.filter(month=month, year=year).order_by("-day")
    data = {
        "Merged": [],
        "Ari": [],
        "Patrick": [],
        "Lippo": [],
    }

    try:
        for report in reports:
            serializer = SmallReportSerializer(report)
            data[serializer.data["author"]].append(serializer.data)
            data["Merged"].append(serializer.data)
    except Exception as e:
        return Response(
            {'error': f'Serializer error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_article(request, id):
    report = Report.objects.get(id=id)

    try:
        serializer = FullReportSerializer(report)
    except Exception as e:
        return Response(
            {'error': f'Serializer error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_news_test(request, month, day, year):
    bouts = Bout.objects.filter(month=month, day=day, year=year)

    serializer = BoutFull(bouts, many=True)

    for bout in serializer.data:
        for side in ["away", "home"]:
            form = bout[side]["performances"][0]["form"]

            change = bout[side]["performances"][0]["previous_rank"] - bout[side]["performances"][0]["rank"]

            if change < 0:
                bout[side]["performances"][0]["ranking_change"] = "Down " + str(abs(change)) + " spot" + ("s" if abs(change) > 1 else "")
            elif change > 0:
                bout[side]["performances"][0]["ranking_change"] = "Up " + str(abs(change)) + " spot" + ("s" if abs(change) > 1 else "")
            else:
                bout[side]["performances"][0]["ranking_change"] = "Rank stays the same"

            unbeaten = 0
            winless = 0
            win = 0
            loss = 0
            unbeaten_broke = False
            winless_broke = False
            win_broke = False
            loss_broke = False

            for ch in form[-2::-1]:
                if unbeaten_broke and winless_broke and win_broke and loss_broke:
                    break
                if ch == 'W':
                    if not win_broke:
                        win += 1
                    if not unbeaten_broke:
                        unbeaten += 1
                    loss_broke = True
                    winless_broke = True
                elif ch == 'L':
                    if not loss_broke:
                        loss += 1
                    if not winless_broke:
                        winless += 1
                    win_broke = True
                    unbeaten_broke = True
                else:
                    if not unbeaten_broke:
                        unbeaten += 1
                    if not winless_broke:
                        winless += 1
                    loss_broke = True
                    win_broke = True
                
            bout[side]["performances"][0]["streaks"] = {
                "unbeaten" : {
                    "count": unbeaten + (0 if form[-1] == 'L' else 1),
                    "type": "snapped" if form[-1] == 'L' else "extended",
                },
                "winless" : {
                    "count": winless + (0 if form[-1] == 'W' else 1),
                    "type": "snapped" if form[-1] == 'W' else "extended",
                },
                "win" : {
                    "count": win + (1 if form[-1] == 'W' else 0),
                    "type": "extended" if form[-1] == 'W' else "snapped",
                },
                "loss" : {
                    "count": loss + (1 if form[-1] == 'L' else 0),
                    "type": "extended" if form[-1] == 'L' else "snapped",
                },
            }

            if (
                bout[side]["performances"][0]["streaks"]["unbeaten"]["count"] < 5 or 
                bout[side]["performances"][0]["streaks"]["unbeaten"]["count"] == bout[side]["performances"][0]["streaks"]["win"]["count"]
            ):
                del bout[side]["performances"][0]["streaks"]["unbeaten"]

            if (
                bout[side]["performances"][0]["streaks"]["winless"]["count"] < 5 or 
                bout[side]["performances"][0]["streaks"]["winless"]["count"] == bout[side]["performances"][0]["streaks"]["loss"]["count"]
            ):
                del bout[side]["performances"][0]["streaks"]["winless"]

            if bout[side]["performances"][0]["streaks"]["win"]["count"] < 3:
                del bout[side]["performances"][0]["streaks"]["win"]

            if bout[side]["performances"][0]["streaks"]["loss"]["count"] < 3:
                del bout[side]["performances"][0]["streaks"]["loss"]

            del bout[side]["performances"][0]["form"]

    return Response({
        "month": month, 
        "day": day, 
        "year": year, 
        "bouts": serializer.data}, 
        status=status.HTTP_200_OK
    )