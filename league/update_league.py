# This code is intended to be run as a standalone script or as part of a scheduled task.
# It will automatically play all bouts that are scheduled to be played before the current time.

from league.models import *
from django.utils import timezone
from typing import List
import random as r
from datetime import datetime, timezone as dt_timezone

PEBBLERS_PER_DIV = 25
NUM_DAYS = 25
LAST_DIVISION = "Learner"

# Setup information needed for running the bouts
rolls = {
    "Power": [1, 1, 2, 5, 5, 6],
    "Grace": [1, 2, 4, 4, 5, 5],
    "Speed": [1, 1, 3, 3, 6, 6],
    "Skill": [1, 3, 3, 4, 4, 6],
}

trigger_rates = {
    "Generosity": 0.36,
    "Will to Win": 0.36,
    "Lucky Seven": 0.12,
    "Miracle": 0.12,
    "Tip the Scales": 0.24,
}

division_stats = {
    "Master"       : {"Quirk": 2, "Ability" : 2},
    "All-Star"     : {"Quirk": 2, "Ability" : 1},
    "Professional" : {"Quirk": 1, "Ability" : 1},
    "Learner"      : {"Quirk": 1, "Ability" : 0},
}

# Note: This is a one-time setup function for setting up the league
# The league will start one month after the year/month specified
def startup_league(year: int, month: int) -> None:
    def create_pebbler_list() -> List[Pebbler]:
        traits = ["Grace", "Skill", "Power", "Speed"]
        quirks = ["Oddball", "Even Temper", "Proud Pebble", "Pity Pebble", "Untouchable"]
        abilities = ["Generosity", "Will to Win", "Lucky Seven", "Miracle", "Tip the Scales"]

        pebbler_names = [
            "Ally", "Ally Jr.", "Almond", "Aurora", "Aversa", "Baby", "Bamboo", "Banji", "Barry", "Beefcake",
            "Berry", "Bert", "Bload", "Bloshi", "Bloshi Jr.", "Bonez", "Brad", "Bumper", "Buzz", "Cammy",
            "Carrotz", "Casey", "Chad", "Chalk", "Chaucer", "Cream", "Croc", "Cuddlez", "Daffy", "Dave",
            "Dominic Bluey", "Doug", "Duke", "Duncan", "Edward", "Ethan", "Felix", "Flapper", "Flippo",
            "Frederick", "Glad", "Gnaf", "Gregory", "Grumps", "Hayley", "Hugz", "Ignatius", "Ima Reddy", "Jiggy",
            "Jolly", "Jonathan", "Juan", "Julie B", "Leo", "Liam", "Logan", "Luke", "Marcel", "Marvin",
            "Matthew", "Mertz", "Monet", "Moshi", "Ness", "Nickelby", "Nut", "Osh", "Owen", "Pabu", "Papa", "Pete",
            "Pigion", "Pinky", "Pip", "Raito", "Road", "Ruby", "Ruth", "Shell", "Shortstop", "Simon",
            "Sir Rocco", "Snow", "Spencer", "Spot", "Sprinkle", "Stewart", "Straw", "Stretch", "Stripe",
            "Taro", "Timmy", "Toast", "Tom", "Tonkotsu", "Tony", "Waddles", "Wasabi", "Watson", "Yoad"
        ]

        used_combinations = set()
        pebbler_info = []

        for i in range(len(pebbler_names)):
            # Ensure unique combinations of trait, quirk, and ability
            while True:
                trait = r.choice(traits)
                quirk = r.choice(quirks)
                ability = r.choice(abilities)
                combo = (trait, quirk, ability)
                if combo not in used_combinations:
                    used_combinations.add(combo)
                    break

            name = f"{r.choice(pebbler_names)}"
            pebbler_names.remove(name)  
            pebbler_info.append({
                "name": name,
                "description": "Member of the Dynamic Dinos. Well-acclimated to windy environments with lots of leaves.",
                "trait": trait,
                "quirk": quirk,
                "ability": ability,
            })

        return pebbler_info
    
    # Create the Pebbler objects in bulk
    pebbler_info = create_pebbler_list()
    for i in range(len(pebbler_info)):
        pebbler_info[i] = Pebbler(
            name=pebbler_info[i]["name"],
            description=pebbler_info[i]["description"],
            trait=pebbler_info[i]["trait"],
            quirk=pebbler_info[i]["quirk"],
            ability=pebbler_info[i]["ability"],
        )
    Pebbler.objects.bulk_create(pebbler_info)
    prepare_next_month(year, month)

def update_league() -> None:
    bouts_to_play = Bout.objects.filter(
        time__lt=timezone.now(),
        away_roll__isnull=True,
    )

    for bout in bouts_to_play:
        play_bout(bout)

def play_bout(bout : Bout) -> None:
    def do_quirks(
        bout : Bout, 
        away_pebbler : Pebbler, 
        away_performance: Performance,
        home_pebbler : Pebbler, 
        home_performance: Performance,
    ) -> None:
        if(
            (away_pebbler.quirk == "Oddball" and bout.away_roll % 2 != bout.day % 2 and bout.home_roll == bout.day % 2) or
            (away_pebbler.quirk == "Even Temper" and bout.away_roll % 2 == bout.day % 2 and bout.home_roll == bout.day % 2) or
            (away_pebbler.quirk == "Pity Pebble" and bout.home_roll - bout.away_roll > 1) or
            (away_pebbler.quirk == "Proud Pebble" and bout.away_roll - bout.home_roll > 1) or
            (away_pebbler.quirk == "Untouchable" and bout.home_roll == 1)
        ):
            bout.away_quirk = True
            bout.away_score += division_stats[bout.division]["Quirk"]
            away_performance.qp += division_stats[bout.division]["Quirk"]
            away_pebbler.qp += division_stats[bout.division]["Quirk"]

        if (
            (home_pebbler.quirk == "Oddball" and bout.home_roll % 2 != bout.day % 2 and bout.away_roll == bout.day % 2) or
            (home_pebbler.quirk == "Even Temper" and bout.home_roll % 2 == bout.day % 2 and bout.away_roll == bout.day % 2) or
            (home_pebbler.quirk == "Pity Pebble" and bout.away_roll - bout.home_roll > 1) or
            (home_pebbler.quirk == "Proud Pebble" and bout.home_roll - bout.away_roll > 1) or
            (home_pebbler.quirk == "Untouchable" and bout.away_roll == 1)
        ):
            bout.home_quirk = True
            bout.home_score += division_stats[bout.division]["Quirk"]
            home_performance.qp += division_stats[bout.division]["Quirk"]
            home_pebbler.qp += division_stats[bout.division]["Quirk"]

    def do_abilities(
        bout : Bout,
        away_pebbler : Pebbler,
        away_performance: Performance,
        home_pebbler : Pebbler,
        home_performance: Performance,
    ) :
        away_draw_mult = 1
        home_draw_mult = 1
        away_win_mult = 1
        home_win_mult = 1
        divison_rate_mult = division_stats[bout.division]["Ability"]

        if away_pebbler.ability == "Generosity":
            if bout.away_roll == bout.home_roll and r.random() < trigger_rates["Generosity"] * divison_rate_mult:
                away_draw_mult = 2; away_performance.at += 1; away_pebbler.at += 1; bout.away_ability = True
        elif away_pebbler.ability == "Will to Win":
            if bout.away_roll == bout.home_roll and r.random() < trigger_rates["Will to Win"] * divison_rate_mult:
                bout.away_roll_half = rolls[away_pebbler.trait][r.randint(0, 5)]
                away_win_mult = 2; away_performance.at += 1; away_pebbler.at += 1; bout.away_ability = True
        elif away_pebbler.ability == "Lucky Seven":
            if bout.away_roll > bout.home_roll and r.random() < trigger_rates["Lucky Seven"] * divison_rate_mult:
                bout.away_roll_half = 7; away_performance.at += 1; away_pebbler.at += 1; bout.away_ability = True
        elif away_pebbler.ability == "Miracle":
            if bout.away_roll < bout.home_roll and r.random() < trigger_rates["Miracle"] * divison_rate_mult:
                bout.away_roll_half = bout.home_roll; away_performance.at += 1; away_pebbler.at += 1; bout.away_ability = True
        else: # Tip the Scales
            if bout.away_roll + 1 == bout.home_roll and r.random() < trigger_rates["Tip the Scales"] * divison_rate_mult:
                bout.away_roll_half = bout.away_roll + 1
                bout.home_roll_half = bout.home_roll - 1
                home_performance.at += 1
                home_pebbler.at += 1
                bout.away_ability = True

        # Update rolls
        if bout.away_roll_half is None:
            bout.away_roll_half = bout.away_roll

        if bout.home_roll_half is None:    
            bout.home_roll_half = bout.home_roll


        if home_pebbler.ability == "Generosity":
            if bout.home_roll_half == bout.away_roll_half and r.random() < trigger_rates["Generosity"] * divison_rate_mult:
                home_draw_mult = 2; home_performance.at += 1; home_pebbler.at += 1; bout.home_ability = True
        elif home_pebbler.ability == "Will to Win":
            if bout.home_roll_half == bout.away_roll_half and r.random() < trigger_rates["Will to Win"] * divison_rate_mult:
                bout.home_roll_final = rolls[home_pebbler.trait][r.randint(0, 5)]
                home_win_mult = 2; home_performance.at += 1; home_pebbler.at += 1; bout.home_ability = True
        elif home_pebbler.ability == "Lucky Seven":
            if bout.home_roll_half > bout.away_roll_half and r.random() < trigger_rates["Lucky Seven"] * divison_rate_mult:
                bout.home_roll_final = 7; home_performance.at += 1; home_pebbler.at += 1; bout.home_ability = True
        elif home_pebbler.ability == "Miracle":
            if bout.home_roll_half < bout.away_roll_half and r.random() < trigger_rates["Miracle"] * divison_rate_mult:
                bout.home_roll_final = bout.away_roll; home_performance.at += 1; home_pebbler.at += 1; bout.home_ability = True
        else: # Tip the Scales
            if bout.home_roll_half + 1 == bout.away_roll_half and r.random() < trigger_rates["Tip the Scales"] * divison_rate_mult:
                bout.away_roll_final = bout.away_roll_half - 1
                bout.home_roll_final = bout.home_roll_half + 1
                home_performance.at += 1
                home_pebbler.at += 1
                bout.home_ability = True

        # Update rolls
        if bout.away_roll_final is None:
            bout.away_roll_final = bout.away_roll_half

        if bout.home_roll_final is None:    
            bout.home_roll_final = bout.home_roll_half

        return away_draw_mult, home_draw_mult, away_win_mult, home_win_mult
        
    # Get the away and home pebbler objects
    away_pebbler = bout.away
    home_pebbler = bout.home

    # Get the away and home performance objects
    away_performance = Performance.objects.get(pebbler=away_pebbler, year=bout.year, month=bout.month)
    home_performance = Performance.objects.get(pebbler=home_pebbler, year=bout.year, month=bout.month)

    # Get the starting rolls
    bout.away_roll = rolls[away_pebbler.trait][r.randint(0, 5)]
    bout.home_roll = rolls[home_pebbler.trait][r.randint(0, 5)]

    do_quirks(bout, away_pebbler, away_performance, home_pebbler, home_performance)

    away_draw_mult, home_draw_mult, away_win_mult, home_win_mult = do_abilities(
        bout, 
        away_pebbler, 
        away_performance, 
        home_pebbler, 
        home_performance
    )

    # Final score calculation
    if bout.away_roll_final == bout.home_roll_final:
        bout.away_score += 3 * (2 * away_draw_mult)
        bout.home_score += 3 * (2 * home_draw_mult)
        away_performance.ties += 1; away_performance.form += "D"
        home_performance.ties += 1; home_performance.form += "D"
    elif bout.away_roll_final > bout.home_roll_final:
        bout.away_score += 3 * (3 * away_win_mult + (bout.away_roll_final - bout.home_roll_final))
        away_performance.wins += 1; away_performance.form += "W"
        home_performance.losses += 1; home_performance.form += "L"
    else:
        bout.home_score += 3 * (3 * home_win_mult + (bout.home_roll_final - bout.away_roll_final))
        away_performance.losses += 1; away_performance.form += "L"
        home_performance.wins += 1; home_performance.form += "W"

    # Update the performances
    away_performance.pebbles += bout.away_score
    away_performance.away_pebbles += bout.away_score
    away_performance.played += 1
    away_performance.away_played += 1
    away_performance.pf += bout.away_roll_final
    away_performance.pa += bout.home_roll_final
    away_performance.pd += bout.away_roll_final - bout.home_roll_final
    away_performance.save()

    home_performance.pebbles += bout.home_score
    home_performance.home_pebbles += bout.home_score
    home_performance.played += 1
    home_performance.home_played += 1
    home_performance.pf += bout.home_roll_final
    home_performance.pa += bout.away_roll_final
    home_performance.pd += bout.home_roll_final - bout.away_roll_final
    home_performance.save()

    # Update pebbler aggregated stats
    away_pebbler.pebbles += bout.away_score
    away_pebbler.away_pebbles += bout.away_score
    away_pebbler.save()

    home_pebbler.pebbles += bout.home_score
    home_pebbler.home_pebbles += bout.home_score
    home_pebbler.save()

    bout.save()

    # Rerank the division if this is the last bout of the day
    if bout.last_in_day:
        rerank_division(bout.division, bout.year, bout.month)
        
        if bout.day == NUM_DAYS and bout.division == LAST_DIVISION:
            prepare_next_month(bout.year, bout.month)
        
def rerank_division(division: str, year: int, month: int) -> None:
    performance_list = Performance.objects.filter(
        division=division,
        year=year,
        month=month,
    ).order_by('-pebbles', '-qp', '-wins', '-ties', '-pd', '-pf', 'tiebreaker')

    for i, performance in enumerate(performance_list):
        performance.previous_rank = performance.rank
        performance.rank = i + 1
        performance.pebbler.current_rank = i + 1
        performance.pebbler.save()
        performance.save()

# 1) Promote and demote based on performances
# 2) Update entries in Pebbler table
# 3) Create new performances for the next month
# 4) Create new bouts for the next month
def prepare_next_month(year: int, month: int) -> None:
    # Create a one indexed schedule for the next month
    def generate_schedule():
        left = []
        right = []
        pebblers = PEBBLERS_PER_DIV
        pebblers += 1 # Bye
        matchups = pebblers // 2

        for i in range(1, pebblers + 1, 2):
            left.append(i)
        for i in range(2, pebblers + 1, 2):
            right.append(i)

        schedule = []

        # Hard coded to ensure each pebblers has equal home and away bouts
        homeAtOne = [2, 6, 10, 14, 18, 22, 5, 9, 13, 17, 21, 25]

        for _ in range(25):
            week_schedule = {"bouts": [], "bye": ""}
            for i in range(matchups):
                if left[i] == pebblers or right[i] == pebblers:
                    week_schedule["bye"] = left[i] if left[i] != pebblers else right[i]
                else:
                    if(i == 0 and right[i] in homeAtOne):
                        week_schedule["bouts"].append({"home": right[i], "away": left[i]})
                    else:
                        week_schedule["bouts"].append({"home": left[i], "away": right[i]})

            schedule.append(week_schedule)

            # Rotate the schedule to create a round robin e.g.
            # 1 2    1 4    1 6    1 5    1 3
            # 3 4    2 6    4 5    6 3    5 2
            # 5 6    3 5    2 3    4 2    6 4

            rightToLeft = right[0]
            leftToRight = left[-1]

            for i in range(pebblers // 2 - 2):
                left[-1 - i] = left[-2 - i]

            for i in range(pebblers // 2 - 1):
                right[i] = right[i + 1]

            right[-1] = leftToRight
            left[1] = rightToLeft

        return schedule
    
    next_year = year + 1 if month == 12 else year
    next_month = 1 if month == 12 else month + 1

    schedule = generate_schedule()

    r.shuffle(schedule)

    for week in schedule:
        r.shuffle(week["bouts"])

    new_divisions = {}
    # If there was not a previous season assign randomly
    if Performance.objects.count() == 0:
        all_pebblers = Pebbler.objects.all()
        start = 0
        for division in ["Master", "All-Star", "Professional", "Learner"]:
            new_divisions[division] = [all_pebblers[i] for i in range(start, start + PEBBLERS_PER_DIV)]
            start += PEBBLERS_PER_DIV
    else:
        for division in ["Master", "All-Star", "Professional", "Learner"]:
            new_divisions[division] = [
                performance.pebbler
                for performance in Performance.objects.filter(
                    year=year, 
                    month=month,
                    division=division,
                ).order_by("rank")
            ]

    # 1) Promote/Demote the bottom 5 from each division
    for i in range(5):
        new_divisions["All-Star"][i], new_divisions["Master"][20 + i] = new_divisions["Master"][20 + i], new_divisions["All-Star"][i]
        new_divisions["Professional"][i], new_divisions["All-Star"][20 + i] = new_divisions["All-Star"][20 + i], new_divisions["Professional"][i]
        new_divisions["Learner"][i], new_divisions["Professional"][20 + i] = new_divisions["Professional"][20 + i], new_divisions["Learner"][i]

    # Update the tables for each division  
    start_hour = 12
    for division in ["Master", "All-Star", "Professional", "Learner"]:
        tiebreakers = [i for i in range(1, 26)]

        for pebbler in new_divisions[division]:
            # 2) Update current division and total division totals 
            pebbler: Pebbler
            pebbler.current_division = division
            match division:
                case "Master":
                    pebbler.masters += 1
                case "All-Star":
                    pebbler.all_stars += 1
                case "Professional":
                    pebbler.professionals += 1
                case "Learner":
                    pebbler.learners += 1
            

            # 3) Add performance for the next month
            tb = r.choice(tiebreakers)
            tiebreakers.remove(tb)
            performance = Performance(
                pebbler=pebbler,
                division=division,
                year=next_year, 
                month=next_month,
                tiebreaker=tb,
                rank=tb,
                previous_rank=tb,
            )

            pebbler.current_rank = tb
            pebbler.save()
            performance.save()

        # 4) Add the bouts for the next month
        for i in range(len(schedule)):
            cur_day = i + 1
            time_ticker = datetime(next_year, next_month, cur_day, start_hour, 0, 0, tzinfo=dt_timezone.utc)
            for j in range(len(schedule[i]["bouts"])):
                Bout.objects.create(
                    away=new_divisions[division][schedule[i]['bouts'][j]['away'] - 1],
                    home=new_divisions[division][schedule[i]['bouts'][j]['home'] - 1],
                    time=time_ticker,
                    division=division,
                    year=next_year,
                    month=next_month,
                    day=cur_day,
                    last_in_day=(j == len(schedule[i]["bouts"]) - 1),
                )
                time_ticker += timezone.timedelta(minutes=10)

        # Matches occur every 10 minutes, and there are 12 matches so we can 
        # increment the hour by 120/2=60 for the next division
        start_hour += 2 


# If there are no pebbler objects, we need to start the league
if Pebbler.objects.count() == 0:
    now = timezone.now()
    current_year = now.year
    current_month = now.month
    # startup_league(current_year, current_month)
    startup_league(2024, 6)
update_league()