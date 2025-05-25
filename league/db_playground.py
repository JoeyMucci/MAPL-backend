from league.models import *
import random as r
from django.utils import timezone

# pebblers = []

# traits = ["Grace", "Power", "Speed", "Skill"]
# quirks = ["Oddball", "Even Temper", "Proud Pebble", "Pity Pebble", "Untouchable"]
# abilities = ["Generosity", "Will to Win", "Lucky Seven", "Miracle", "Tip the Scales"]

# i = 1
# for trait in traits:
#     for quirk in quirks:
#         for ability in abilities:
#             pebbler = Pebbler(
#                 name=f"Pebbler {i}", 
#                 trait=trait,
#                 quirk=quirk,
#                 ability=ability
#             )
#             pebblers.append(pebbler)
#             i += 1

# # Create the Pebbler objects in bulk
# Pebbler.objects.bulk_create(pebblers)  


# i = 1
# for division in ["Master", "All-Star", "Professional", "Learner"]:
#     tiebreakers = [i for i in range(1, 26)]
#     r.shuffle(tiebreakers)
    
#     for j in range(25):
#         p = Performance(
#             pebbler=Pebbler.objects.get(name=f"Pebbler {i}"),
#             division=division,
#             year=2025, 
#             month=6,
#             tiebreaker=tiebreakers[j],
#             rank=tiebreakers[j],
#             previous_rank=tiebreakers[j],
#         )
#         p.save()
#         i += 1

def generate_schedule():
    left = []
    right = []
    pebblers = 25
    pebblers += 1 # Bye
    matchups = pebblers // 2

    for i in range(1, pebblers + 1, 2):
        left.append(i)
    for i in range(2, pebblers + 1, 2):
        right.append(i)

    schedule = []

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

        rightToLeft = right[0]
        leftToRight = left[-1]

        for i in range(pebblers // 2 - 2):
            left[-1 - i] = left[-2 - i]

        for i in range(pebblers // 2 - 1):
            right[i] = right[i + 1]

        right[-1] = leftToRight
        left[1] = rightToLeft

    return schedule

schedule = generate_schedule()

time_ticker = timezone.now()

for division in ["Master", "All-Star", "Professional", "Learner"]:
    pebbler_names = list(
        Pebbler.objects.filter(current_division=division)
        .values_list('name', flat=True)
    )
    r.shuffle(pebbler_names)
    pebbler_names.insert(0, "Bye") # Insert a dummy for indexing

    day_num = 1
    for day in schedule: 
        for bout in day["bouts"]:
            time = time_ticker
            time_ticker += timezone.timedelta(minutes=1)
            bout_obj = Bout(
                home=Pebbler.objects.get(name=pebbler_names[bout["home"]]),
                away=Pebbler.objects.get(name=pebbler_names[bout["away"]]),
                time=time,
                division=division,
                year=2025,
                month=6,
                day=day_num
            )
            bout_obj.save()
        day_num += 1