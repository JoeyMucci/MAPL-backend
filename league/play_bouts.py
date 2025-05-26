from league.models import *
from django.utils import timezone
import random as r

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

def play_bouts():
    bouts_to_play = Bout.objects.filter(
        time__lt=timezone.now(),
        away_roll__isnull=True,
    )

    for bout in bouts_to_play:
        # Get the away and home pebbler objects
        away_pebbler = bout.away
        home_pebbler = bout.home

        # Get the away and home performance objects
        away_performance = Performance.objects.get(pebbler=away_pebbler, year=bout.year, month=bout.month)
        home_performance = Performance.objects.get(pebbler=home_pebbler, year=bout.year, month=bout.month)

        # Get the starting rolls
        bout.away_roll = rolls[away_pebbler.trait][r.randint(0, 5)]
        bout.home_roll = rolls[home_pebbler.trait][r.randint(0, 5)]

        # Quirk effects
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

        # Ability effects
        away_draw_mult = 1
        home_draw_mult = 1
        away_win_mult = 1
        home_win_mult = 1
        divison_rate_mult = division_stats[bout.division]["Ability"]

        if away_pebbler.ability == "Generosity":
            if bout.away_roll == bout.home_roll and r.random() < trigger_rates["Generosity"] * divison_rate_mult:
                away_draw_mult = 2; away_performance.at += 1; away_pebbler.at += 1
        elif away_pebbler.ability == "Will to Win":
            if bout.away_roll == bout.home_roll and r.random() < trigger_rates["Will to Win"] * divison_rate_mult:
                bout.away_roll_half = rolls[away_pebbler.trait][r.randint(0, 5)]
                away_win_mult = 2; away_performance.at += 1; away_pebbler.at += 1
        elif away_pebbler.ability == "Lucky Seven":
            if bout.away_roll > bout.home_roll and r.random() < trigger_rates["Lucky Seven"] * divison_rate_mult:
                bout.away_roll_half = 7; away_performance.at += 1; away_pebbler.at += 1
        elif away_pebbler.ability == "Miracle":
            if bout.away_roll < bout.home_roll and r.random() < trigger_rates["Miracle"] * divison_rate_mult:
                bout.away_roll_half = bout.home_roll; away_performance.at += 1; away_pebbler.at += 1
        else: # Tip the Scales
            if bout.away_roll + 1 == bout.home_roll and r.random() < trigger_rates["Tip the Scales"] * divison_rate_mult:
                bout.away_roll_half = bout.away_roll + 1
                bout.home_roll_half = bout.home_roll - 1
                home_performance.at += 1
                home_pebbler.at += 1

        # Update rolls
        if bout.away_roll_half is None:
            bout.away_roll_half = bout.away_roll

        if bout.home_roll_half is None:    
            bout.home_roll_half = bout.home_roll


        if home_pebbler.ability == "Generosity":
            if bout.home_roll_half == bout.away_roll_half and r.random() < trigger_rates["Generosity"] * divison_rate_mult:
                home_draw_mult = 2; home_performance.at += 1; home_pebbler.at += 1
        elif home_pebbler.ability == "Will to Win":
            if bout.home_roll_half == bout.away_roll_half and r.random() < trigger_rates["Will to Win"] * divison_rate_mult:
                bout.home_roll_final = rolls[home_pebbler.trait][r.randint(0, 5)]
                home_win_mult = 2; home_performance.at += 1; home_pebbler.at += 1
        elif home_pebbler.ability == "Lucky Seven":
            if bout.home_roll_half > bout.away_roll_half and r.random() < trigger_rates["Lucky Seven"] * divison_rate_mult:
                bout.home_roll_final = 7; home_performance.at += 1; home_pebbler.at += 1
        elif home_pebbler.ability == "Miracle":
            if bout.home_roll_half < bout.away_roll_half and r.random() < trigger_rates["Miracle"] * divison_rate_mult:
                bout.home_roll_final = bout.away_roll; home_performance.at += 1; home_pebbler.at += 1
        else: # Tip the Scales
            if bout.home_roll_half + 1 == bout.away_roll_half and r.random() < trigger_rates["Tip the Scales"] * divison_rate_mult:
              bout.away_roll_final = bout.away_roll_half - 1
              bout.home_roll_final = bout.home_roll_half + 1
              home_performance.at += 1
              home_pebbler.at += 1

        # Update rolls
        if bout.away_roll_final is None:
            bout.away_roll_final = bout.away_roll_half

        if bout.home_roll_final is None:    
            bout.home_roll_final = bout.home_roll_half


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


play_bouts()