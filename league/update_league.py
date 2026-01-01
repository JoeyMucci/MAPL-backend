# This code is intended to be run as a standalone script or as part of a scheduled task.
# It will automatically play all bouts that are scheduled to be played before the current time.

from league.models import *
from django.utils import timezone
import random as r
import importlib
import league.setup_vars as sv
importlib.reload(sv)
from datetime import datetime, timezone as dt_timezone

# Note: This is a one-time setup function for setting up the league
# The league will start one month after the year/month specified
def startup_league(year: int, month: int) -> None:
    # Create the Pebbler objects in bulk
    pebbler_info = sv.pebbler_list.copy()
    for i in range(len(pebbler_info)):
        pebbler_info[i] = Pebbler(
            name=pebbler_info[i]["name"],
            description=pebbler_info[i]["description"],
            isMale=pebbler_info[i]["isMale"],
            trait=pebbler_info[i]["trait"],
            quirk=pebbler_info[i]["quirk"],
            ability=pebbler_info[i]["ability"],
        )
    Pebbler.objects.bulk_create(pebbler_info)
    prepare_next_month(year, month)

def update_league() -> None:
    cur_time = timezone.now() if sv.real_time else datetime(sv.cur_year, sv.cur_month, sv.cur_day, 23, 59, 0, tzinfo=dt_timezone.utc)

    bouts_to_play = Bout.objects.filter(
        time__lt=cur_time,
        away_roll__isnull=True,
    ).order_by('time')

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
            (away_pebbler.quirk == "Oddball" and bout.away_roll % 2 != bout.day % 2 and bout.home_roll % 2 == bout.day % 2) or
            (away_pebbler.quirk == "Even Temper" and bout.away_roll % 2 == bout.day % 2 and bout.home_roll % 2 == bout.day % 2) or
            (away_pebbler.quirk == "Pity Pebble" and bout.home_roll - bout.away_roll > 1) or
            (away_pebbler.quirk == "Proud Pebble" and bout.away_roll - bout.home_roll > 1) or
            (away_pebbler.quirk == "Untouchable" and bout.home_roll == 1)
        ):
            bout.away_quirk = True
            bout.away_score += sv.division_stats[bout.division]["Quirk"]
            away_performance.qp += sv.division_stats[bout.division]["Quirk"]
            away_pebbler.qp += sv.division_stats[bout.division]["Quirk"]
            away_pebbler.ytd_qp += sv.division_stats[bout.division]["Quirk"]

        if (
            (home_pebbler.quirk == "Oddball" and bout.home_roll % 2 != bout.day % 2 and bout.away_roll % 2 == bout.day % 2) or
            (home_pebbler.quirk == "Even Temper" and bout.home_roll % 2 == bout.day % 2 and bout.away_roll % 2 == bout.day % 2) or
            (home_pebbler.quirk == "Pity Pebble" and bout.away_roll - bout.home_roll > 1) or
            (home_pebbler.quirk == "Proud Pebble" and bout.home_roll - bout.away_roll > 1) or
            (home_pebbler.quirk == "Untouchable" and bout.away_roll == 1)
        ):
            bout.home_quirk = True
            bout.home_score += sv.division_stats[bout.division]["Quirk"]
            home_performance.qp += sv.division_stats[bout.division]["Quirk"]
            home_pebbler.qp += sv.division_stats[bout.division]["Quirk"]
            home_pebbler.ytd_qp += sv.division_stats[bout.division]["Quirk"]

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
        divison_rate_mult = sv.division_stats[bout.division]["Ability"]

        if away_pebbler.ability == "Generosity":
            if bout.away_roll == bout.home_roll and r.random() < sv.trigger_rates["Generosity"] * divison_rate_mult:
                away_draw_mult = 2; away_performance.at += 1; away_pebbler.at += 1; away_pebbler.ytd_at += 1; bout.away_ability = True
        elif away_pebbler.ability == "Will to Win":
            if bout.away_roll == bout.home_roll and r.random() < sv.trigger_rates["Will to Win"] * divison_rate_mult:
                bout.away_roll_half = sv.rolls[away_pebbler.trait][r.randint(0, 5)]
                away_win_mult = 2; away_performance.at += 1; away_pebbler.at += 1; away_pebbler.ytd_at += 1; bout.away_ability = True
        elif away_pebbler.ability == "Lucky Seven":
            if bout.away_roll > bout.home_roll and r.random() < sv.trigger_rates["Lucky Seven"] * divison_rate_mult:
                bout.away_roll_half = 7; away_performance.at += 1; away_pebbler.at += 1; away_pebbler.ytd_at += 1; bout.away_ability = True
        elif away_pebbler.ability == "Miracle":
            if bout.away_roll < bout.home_roll and r.random() < sv.trigger_rates["Miracle"] * divison_rate_mult:
                bout.away_roll_half = bout.home_roll; away_performance.at += 1; away_pebbler.at += 1; away_pebbler.ytd_at += 1; bout.away_ability = True
        else: # Tip the Scales
            if bout.away_roll + 1 == bout.home_roll and r.random() < sv.trigger_rates["Tip the Scales"] * divison_rate_mult:
                bout.away_roll_half = bout.away_roll + 1
                bout.home_roll_half = bout.home_roll - 1
                away_performance.at += 1
                away_pebbler.at += 1
                away_pebbler.ytd_at += 1
                bout.away_ability = True

        # Update rolls
        if bout.away_roll_half is None:
            bout.away_roll_half = bout.away_roll

        if bout.home_roll_half is None:    
            bout.home_roll_half = bout.home_roll


        if home_pebbler.ability == "Generosity":
            if bout.home_roll_half == bout.away_roll_half and r.random() < sv.trigger_rates["Generosity"] * divison_rate_mult:
                home_draw_mult = 2; home_performance.at += 1; home_pebbler.at += 1; home_pebbler.ytd_at += 1; bout.home_ability = True
        elif home_pebbler.ability == "Will to Win":
            if bout.home_roll_half == bout.away_roll_half and r.random() < sv.trigger_rates["Will to Win"] * divison_rate_mult:
                bout.home_roll_final = sv.rolls[home_pebbler.trait][r.randint(0, 5)]
                home_win_mult = 2; home_performance.at += 1; home_pebbler.at += 1; home_pebbler.ytd_at += 1; bout.home_ability = True
        elif home_pebbler.ability == "Lucky Seven":
            if bout.home_roll_half > bout.away_roll_half and r.random() < sv.trigger_rates["Lucky Seven"] * divison_rate_mult:
                bout.home_roll_final = 7; home_performance.at += 1; home_pebbler.at += 1; home_pebbler.ytd_at += 1; bout.home_ability = True
        elif home_pebbler.ability == "Miracle":
            if bout.home_roll_half < bout.away_roll_half and r.random() < sv.trigger_rates["Miracle"] * divison_rate_mult:
                bout.home_roll_final = bout.away_roll_half; home_performance.at += 1; home_pebbler.at += 1; home_pebbler.ytd_at += 1; bout.home_ability = True
        else: # Tip the Scales
            if bout.home_roll_half + 1 == bout.away_roll_half and r.random() < sv.trigger_rates["Tip the Scales"] * divison_rate_mult:
                bout.away_roll_final = bout.away_roll_half - 1
                bout.home_roll_final = bout.home_roll_half + 1
                home_performance.at += 1
                home_pebbler.at += 1
                home_pebbler.ytd_at += 1
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
    bout.away_roll = sv.rolls[away_pebbler.trait][r.randint(0, 5)]
    bout.home_roll = sv.rolls[home_pebbler.trait][r.randint(0, 5)]

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
        away_performance.ties += 1; away_performance.form += "T"
        home_performance.ties += 1; home_performance.form += "T"
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
    away_pebbler.ytd_pebbles += bout.away_score
    away_pebbler.ytd_away_pebbles += bout.away_score
    away_pebbler.save()

    home_pebbler.pebbles += bout.home_score
    home_pebbler.home_pebbles += bout.home_score
    home_pebbler.ytd_pebbles += bout.home_score
    home_pebbler.ytd_home_pebbles += bout.home_score
    home_pebbler.save()

    bout.save()

    if bout.last_in_day:
        rerank_divisions(bout.year, bout.month)

        # Prepare the next month if this is the last bout of the month
        if bout.day == sv.num_days:
            prepare_next_month(bout.year, bout.month)

def get_next_day(year: int, month: int, day: int) -> tuple[int, int, int]:
    new_day = day + 1
    new_month = month
    new_year = year
    if new_day > sv.num_days:
        new_day = 1
        new_month += 1
        if new_month > 12:
            new_month = 1
            new_year += 1
    return new_year, new_month, new_day


def rerank_divisions(year: int, month: int) -> None:
    for division in sv.divisions:
        rerank_division(division, year, month)
        
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

# 1) Promote/Demote the bottom 5 from each division
# 2) Update entries in Pebbler table
# 3) Create new performances for the next month
# 4) Create new bouts for the next month
def prepare_next_month(year: int, month: int) -> None:
    next_year = year + 1 if month == 12 else year
    next_month = 1 if month == 12 else month + 1
    
    schedule = sv.generate_schedule()

    r.shuffle(schedule)

    for week in schedule:
        r.shuffle(week["bouts"])

    new_divisions = {}
    # If there was not a previous season assign randomly
    if Performance.objects.count() == 0:
        all_pebblers = list(Pebbler.objects.all())
        r.shuffle(all_pebblers)
        start = 0
        for division in sv.divisions:
            new_divisions[division] = all_pebblers[start:start + sv.pebblers_per_div]
            start += sv.pebblers_per_div
    else:
        for division in sv.divisions:
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
    start_minutes = 0
    for division in sv.divisions:
        tiebreakers = [i for i in range(1, 26)]

        for pebbler in new_divisions[division]:
            # 2) Update entries in Pebbler table
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

            # Wipe YTD stats if starting new year
            if next_month == 1:
                pebbler.ytd_pebbles = 0
                pebbler.ytd_away_pebbles = 0
                pebbler.ytd_home_pebbles = 0
                pebbler.ytd_qp = 0
                pebbler.ytd_at = 0

            # 3) Create new performances for the next month
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

        # 4) Create new bouts for the next month
        for i in range(len(schedule)):
            cur_day = i + 1
            time_ticker = datetime(next_year, next_month, cur_day, 12, start_minutes, 0, tzinfo=dt_timezone.utc)
            for j in range(len(schedule[i]["bouts"])):
                Bout.objects.create(
                    away=new_divisions[division][schedule[i]['bouts'][j]['away'] - 1],
                    home=new_divisions[division][schedule[i]['bouts'][j]['home'] - 1],
                    time=time_ticker,
                    division=division,
                    year=next_year,
                    month=next_month,
                    day=cur_day,
                    last_in_day=(j == len(schedule[i]["bouts"]) - 1 and division == sv.last_division),
                )
                time_ticker += timezone.timedelta(minutes=40)

        # Matches occur every 10 minutes, and there are 12 matches so we can 
        # increment the hour by 120/2=60 for the next division
        start_minutes += 10

    update_league() # Try and play the bouts that were just created


# If there are no pebbler objects, we need to start the league
if Pebbler.objects.count() == 0:
    startup_league(sv.start_year, sv.start_month)
else:
    update_league()