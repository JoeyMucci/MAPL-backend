from league.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_news(request, month, day, year):
    bouts = Bout.objects.filter(month=month, day=day, year=year)

    serializer = BoutFull(bouts, many=True)

    for bout in serializer.data:
        for side in ["away", "home"]:
            form = bout[side]["performances"][0]["form"]

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