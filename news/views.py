from news.models import *
from news.serializers import *
import random as r
from rest_framework.response import Response
from rest_framework import status
import re
from rest_framework.decorators import api_view

divisions = ["Master", "All-Star", "Professional", "Learner"]
RANKINGS_THRESHOLD = 3
PROMOTE_DEMOTE_THRESHOLD = 13
FINAL_DAY = 25
BOUTS_PER_DIV = 12
MAX_BOUTS = 8

abilityActionMap = {
    "Miracle": "upgrades roll to opponent's roll",
    "Lucky Seven": "upgrades roll to 7",
    "Generosity": "doubles tie bonus",
    "Will to Win": "rerolls and doubles win bonus",
    "Tip the Scales": "switches roll with opponent",
}

def camelcase_to_words(s):
    words = re.sub('([a-z])([A-Z])', r'\1 \2', s)
    return words.title()

@api_view(['GET'])
def get_author(request, authorName):
    author_name = camelcase_to_words(authorName)

    try:
        author = Reporter.objects.get(name=author_name)
    except Reporter.DoesNotExist:
        return Response(
            {'error': 'Reporter not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        serializer = ReporterSerializer(author)
        serialized_author = serializer.data
    except Exception as e:
        return Response(
            {'error': f'Serializing error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response(serialized_author, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_helper(request, helperName):
    helper_name = camelcase_to_words(helperName)

    try:
        helper = Referee.objects.get(name=helper_name)
    except Referee.DoesNotExist:
        return Response(
            {'error': 'Referee not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        serializer = RefereeSerializer(helper)
        serialized_helper = serializer.data
    except Exception as e:
        return Response(
            {'error': f'Serializing error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response(serialized_helper, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_news_by_month(request, month, year):
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
            {'error': f'Serializing error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_news_by_day(request, month, year, day):
    reports = Report.objects.filter(month=month, year=year, day=day)
    if len(reports) != 1:
        return Response(
            {'error': 'Report not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        for report in reports:
            serializer = SmallReportSerializer(report)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Serializing error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_article(request, id):
    report = Report.objects.get(id=id)

    try:
        serializer = FullReportSerializer(report)
    except Exception as e:
        return Response(
            {'error': f'Serializing error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response(serializer.data, status=status.HTTP_200_OK)

# Return the last 5 articles
@api_view(['GET'])
def get_hot_press(request):
    reports = Report.objects.order_by('-year', '-month', '-day')[:5]

    try:
        serializer = SmallReportSerializer(reports, many=True)
    except Exception as e:
        return Response(
            {'error': f'Serializing error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_news_test(request, month, day, year):
    try:
        bouts = Bout.objects.filter(month=month, day=day, year=year, away_roll__isnull=False)
        data = get_claude_data(bouts, day)
    except Exception as e:
        return Response(
            {'error': f'Error: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response({
        "month": month, 
        "day": day, 
        "year": year, 
        "bouts": data}, 
        status=status.HTTP_200_OK
    )

def get_claude_data(bouts, day):
    auto = []
    notable = []
    serializer = BoutFull(bouts, many=True)
    bts = serializer.data
    r.shuffle(bts)
    auto_bout = { division : None for division in divisions}
    notable_bout = {division : None for division in divisions}
    div_mp = {division : 0 for division in divisions}

    for bout in bts:
        rel = False
        ranking_bookend = False
        div = bout["division"]
        data = {}
        data["division"] = div
        data["time"] = bout["time"]
        data["notable_circumstances"] = []

        data["away"] = {}
        data["home"] = {}
        data["away"]["name"] = bout["away"]["name"]
        data["away"]["description"] = bout["away"]["description"]
        data["home"]["name"] = bout["home"]["name"]
        data["home"]["description"] = bout["home"]["description"]
        data["away"]["gender"] = "Male" if bout["away"]["isMale"] else "Female"
        data["home"]["gender"] = "Male" if bout["home"]["isMale"] else "Female"

        if bout["away"]["description"].split(".")[0] == bout["home"]["description"].split(".")[0]:
            data["notable_circumstances"].append(f"Pebblers are members of same group: '{bout["away"]["description"].split(".")[0].split('the ', 1)[1] }'")
            rel = True

        if (
            data["away"]["name"] == "Julie B." and "Yellow Fellows" in bout["home"]["description"]
            or data["home"]["name"] == "Julie B." and "Yellow Fellows" in bout["away"]["description"]
        ):
            data["notable_circumstances"].append(f"Honorary member meets member: 'Yellow Fellows'")
            rel = True

        if (
            data["away"]["name"] == "Pip" and "emperors of the Pebble Kingdom" in bout["home"]["description"]
            or data["home"]["name"] == "Pip" and "emperors of the Pebble Kingdom" in bout["away"]["description"]
        ):
            data["notable_circumstances"].append(f"Honorary member meets member: 'emperors of the Pebble Kingdom'")
            rel = True

        if data["away"]["name"] in data["home"]["description"].split(".")[0] or data["home"]["name"] in data["away"]["description"].split(".")[0]:
            away_str = ""
            home_str = ""

            if data["away"]["name"] in data["home"]["description"]:
                home_str = f"{data["home"]["name"]}: {data["home"]["description"].split(".")[0]}"

            if data["home"]["name"] in data["away"]["description"]:
                away_str = f"{data["away"]["name"]}: {data["away"]["description"].split(".")[0]}"

            data["notable_circumstances"].append(f"Pebblers have a personal relationship. {away_str}{"; " if away_str and home_str else ""}{home_str}")
            rel = True
        
        away_qp = 0
        home_qp = 0
        data["bout_events"] = {}
        data["bout_events"]["initial_roll"] = {
            "away": f"{data["away"]["name"]} rolls a {bout["away_roll"]} with '{bout["away"]["trait"]}' trait",
            "home": f"{data["home"]["name"]} rolls a {bout["home_roll"]} with '{bout["home"]["trait"]}' trait",
        }
        data["bout_events"]["initial_rolls"] = f"{data["away"]["name"]}: {bout["away_roll"]} - {bout["home"]["name"]}: {bout["home_roll"]}"
        data["bout_events"]["quirk_activations"] = {"away" : None, "home": None}
        if bout["away_quirk"]:
            data["bout_events"]["quirk_activations"]["away"] = f"{data["away"]["name"]} gains {"2 pebbles" if div in divisions[:2] else "1 pebble"} with '{bout["away"]["quirk"]}' quirk"
            away_qp = 2 if div in divisions[:2] else 1
        if bout["home_quirk"]:
            data["bout_events"]["quirk_activations"]["home"] = f"{data["home"]["name"]} gains {"2 pebbles" if div in divisions[:2] else "1 pebble"} with '{bout["home"]["quirk"]}' quirk"
            home_qp = 2 if div in divisions[:2] else 1
        data["bout_events"]["away_ability_trigger"] = None
        if bout["away_ability"]:
            data["bout_events"]["away_ability_trigger"] = f"{data["away"]["name"]} {abilityActionMap[bout["away"]["ability"]]} with '{bout["away"]["ability"]}' ability"
        data["bout_events"]["halftime_rolls"] = f"{data["away"]["name"]}: {bout["away_roll_half"]} - {bout["home"]["name"]}: {bout["home_roll_half"]}"
        data["bout_events"]["home_ability_trigger"] = None
        if bout["home_ability"]:
            data["bout_events"]["home_ability_trigger"] = f"{data["home"]["name"]} {abilityActionMap[bout["home"]["ability"]]} with '{bout["home"]["ability"]}' ability"
        data["bout_events"]["final_rolls"] = f"{data["away"]["name"]}: {bout["away_roll_final"]} - {bout["home"]["name"]}: {bout["home_roll_final"]}"

        awayResult = None
        homeResult = None
        if bout["away_roll_final"] is not None and bout["home_roll_final"] is not None:
            if bout["away_roll_final"] > bout["home_roll_final"]:
                awayResult = "winning"
                homeResult = "losing"
            elif bout["away_roll_final"] < bout["home_roll_final"]:
                homeResult = "winning"
                awayResult = "losing"
            else:
                awayResult = "tying"
                homeResult = "tying"
            
        data["bout_events"]["results"] = {
            "away": f"{bout["away"]["name"]} gains {bout["away_score"] - away_qp} pebbles from {awayResult}",
            "home": f"{bout["home"]["name"]} gains {bout["home_score"] - home_qp} pebbles from {homeResult}",
        }
        data["bout_events"]["total_pebbles"] = {
            "away": f"{bout["away"]["name"]}: {bout["away_score"]}",
            "home": f"{bout["home"]["name"]}: {bout["home_score"]}",
        }

        if day >= RANKINGS_THRESHOLD:
            data["updated_notable_streaks"] = {}
            data["updated_ranking"] = {}
        if day == FINAL_DAY:
            data["updated_division"] = {}
        elif day >= PROMOTE_DEMOTE_THRESHOLD:
            data["promotion/demotion_status"] = {}
        for side in ["away", "home"]:
            

            # Add ranking change and streaks
            if day >= RANKINGS_THRESHOLD:
                data["updated_ranking"][side] = {}
                change = bout[side]["performances"][0]["previous_rank"] - bout[side]["performances"][0]["rank"]

                if change < 0:
                    data["updated_ranking"][side]["ranking_change"] = "Down " + str(abs(change)) + " place" + ("s" if abs(change) > 1 else "")
                elif change > 0:
                    data["updated_ranking"][side]["ranking_change"] = "Up " + str(abs(change)) + " place" + ("s" if abs(change) > 1 else "")
                else:
                    data["updated_ranking"][side]["ranking_change"] = "Rank stays the same"

                data["updated_ranking"][side]["updated_rank"] = bout[side]["performances"][0]["rank"]
                data["updated_ranking"][side]["previous_rank"] = bout[side]["performances"][0]["previous_rank"]


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

                if win >= 5:
                    data["notable_circumstances"].append(f"{data[side]["name"]} is on a {win} bout winning streak")
                if loss >= 5:
                    data["notable_circumstances"].append(f"{data[side]["name"]} is on a {loss} bout losing streak")
                if unbeaten >= 9:
                    data["notable_circumstances"].append(f"{data[side]["name"]} is on a {unbeaten} bout unbeaten streak")
                if winless >= 9:
                    data["notable_circumstances"].append(f"{data[side]["name"]} is on a {winless} bout winless streak")

                if len(form) > 0:
                    data["updated_notable_streaks"][side] = {
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
                    data["updated_notable_streaks"][side]["unbeaten"]["count"] < 5 or 
                    data["updated_notable_streaks"][side]["unbeaten"]["count"] == data["updated_notable_streaks"][side]["win"]["count"]
                    ):
                        del data["updated_notable_streaks"][side]["unbeaten"]

                    if (
                    data["updated_notable_streaks"][side]["winless"]["count"] < 5 or 
                    data["updated_notable_streaks"][side]["winless"]["count"] == data["updated_notable_streaks"][side]["loss"]["count"]
                    ):
                        del data["updated_notable_streaks"][side]["winless"]

                    if data["updated_notable_streaks"][side]["win"]["count"] < 3:
                        del data["updated_notable_streaks"][side]["win"]

                    if data["updated_notable_streaks"][side]["loss"]["count"] < 3:
                        del data["updated_notable_streaks"][side]["loss"]

            # More explicit labeling for the final day
            if day == FINAL_DAY:
                result = f"Stayed in {div}"

                if bout[side]["performances"][0]["rank"] <= 5 and div != divisions[0]:
                    idx = divisions.index(div)
                    result = f"Promoted to {divisions[idx - 1]}"
                elif bout[side]["performances"][0]["rank"] >= 21 and div != divisions[-1]:
                    idx = divisions.index(div)
                    result = f"Demoted to {divisions[idx + 1]}"

                data["updated_division"][side] = result
            elif day >= PROMOTE_DEMOTE_THRESHOLD:
                idx = divisions.index(div)
                if idx != 0 and data["updated_ranking"][side]["updated_rank"] <= 5:
                    data["promotion/demotion_status"][side] = f"In position for promotion to {divisions[idx - 1]}"
                elif idx != 0 and data["updated_ranking"][side]["updated_rank"] <= 9:
                    data["promotion/demotion_status"][side] = f"Just outside position for promotion to {divisions[idx - 1]}"
                elif idx != len(divisions) - 1 and data["updated_ranking"][side]["updated_rank"] >= 21:
                    data["promotion/demotion_status"][side] = f"In position for demotion to {divisions[idx + 1]}"
                elif idx != len(divisions) - 1 and data["updated_ranking"][side]["updated_rank"] >= 17:
                    data["promotion/demotion_status"][side] = f"Just outside position for demotion to {divisions[idx + 1]}"
                elif idx == 0 and data["updated_ranking"][side]["updated_rank"] <= 5:
                    data["promotion/demotion_status"][side] = f"Cannot be promoted from {divisions[0]} division"
                elif idx == len(divisions) - 1 and data["updated_ranking"][side]["updated_rank"] >= 21:
                    data["promotion/demotion_status"][side] = f"Cannot be demoted from {divisions[-1]} division"
                else:
                    data["promotion/demotion_status"][side] = "Not in position for promotion/demotion"


        if day >= RANKINGS_THRESHOLD:
            if data["updated_ranking"]["away"]["previous_rank"] <= 5 and data["updated_ranking"]["home"]["previous_rank"] <= 5:
                data["notable_circumstances"].append("Bout between two top 5 pebblers")
                ranking_bookend = True

            if data["updated_ranking"]["away"]["previous_rank"] >= 21 and data["updated_ranking"]["home"]["previous_rank"] >= 21:
                data["notable_circumstances"].append("Bout between two bottom 5 pebblers")
                ranking_bookend = True

        div_mp[div] += 1

        if (
            data["bout_events"]["away_ability_trigger"] and data["bout_events"]["home_ability_trigger"]
            or rel
            or ranking_bookend and (data["bout_events"]["away_ability_trigger"] or  data["bout_events"]["home_ability_trigger"] or (len([value for value in data["bout_events"]["quirk_activations"].values() if value is not None]) == 2 and div == divisions[-1]))
        ):
            if auto_bout[div]:
                auto.append(data)
            else:
                if notable_bout[div]:
                    notable.append(notable_bout[div])
                    notable_bout[div] = None
                auto_bout[div] = data

        elif (
            len(data["notable_circumstances"]) > 0 or 
            len([value for value in data["bout_events"]["quirk_activations"].values() if value is not None]) == 2 and div == divisions[-1] or 
            data["bout_events"]["away_ability_trigger"] or data["bout_events"]["home_ability_trigger"]
        ):
            if auto_bout[div] or notable_bout[div]:
                notable.append(data)
            else:
                notable_bout[div] = data

        elif not auto_bout[div] and not notable_bout[div] and div_mp[div] == BOUTS_PER_DIV:
            notable_bout[div] = data

    bouts_to_report = []
    for divvy in divisions:
        if auto_bout[divvy]:
            bouts_to_report.append(auto_bout[divvy])
        else:
            bouts_to_report.append(notable_bout[divvy])

    auto.extend(notable)
    for elem in auto:
        if len(bouts_to_report) < MAX_BOUTS:
            bouts_to_report.append(elem)

    bouts_to_report.sort(key=lambda bout : bout["time"])

    return bouts_to_report