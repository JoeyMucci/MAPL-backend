__all__ = [
    "pebblers_per_div", "num_days", "last_division", "start_year", "start_month",
    "real_time", "cur_year", "cur_month", "cur_day", "pebbler_list",
    "rolls" ,"trigger_rates", "division_stats", "generate_schedule",
]

pebblers_per_div = 25
num_days = 25
last_division = "Learner"

start_year = 2023
start_month = 1

# REAL_TIME determines whether or not to use to actual time, set to false and modify
# CUR_YEAR, CUR_MONTH, and CUR_DAY to test the league running for certain amount of time
real_time = True
cur_year = 2023
cur_month = 1
cur_day = 10

pebbler_list = [
    ["Cammy", "Grace", "Oddball", "Generosity"],
    ["Edward", "Grace", "Oddball", "Will to Win"],
    ["Jiggy", "Grace", "Oddball", "Lucky Seven"],
    ["Snow", "Grace", "Oddball", "Miracle"],
    ["Stretch", "Grace", "Oddball", "Tip the Scales"],
    ["Hugz", "Grace", "Even Temper", "Generosity"],
    ["Sir Rocco", "Grace", "Even Temper", "Will to Win"],
    ["Casey", "Grace", "Even Temper", "Lucky Seven"],
    ["Banji", "Grace", "Even Temper", "Miracle"],
    ["Liam", "Grace", "Even Temper", "Tip the Scales"],
    ["Tonkotsu", "Grace", "Proud Pebble", "Generosity"],
    ["Papa", "Grace", "Proud Pebble", "Will to Win"],
    ["Toast", "Grace", "Proud Pebble", "Lucky Seven"],
    ["Straw", "Grace", "Proud Pebble", "Miracle"],
    ["Monet", "Grace", "Proud Pebble", "Tip the Scales"],
    ["Bamboo", "Grace", "Pity Pebble", "Generosity"],
    ["Baby", "Grace", "Pity Pebble", "Will to Win"],
    ["Owen", "Grace", "Pity Pebble", "Lucky Seven"],
    ["Matthew", "Grace", "Pity Pebble", "Miracle"],
    ["Ness", "Grace", "Pity Pebble", "Tip the Scales"],
    ["Gnaf", "Grace", "Untouchable", "Generosity"],
    ["Sprinkle", "Grace", "Untouchable", "Will to Win"],
    ["Aversa", "Grace", "Untouchable", "Lucky Seven"],
    ["Jonathan", "Grace", "Untouchable", "Miracle"],
    ["Flippo", "Grace", "Untouchable", "Tip the Scales"],
    ["Ethan", "Skill", "Oddball", "Generosity"],
    ["Logan", "Skill", "Oddball", "Will to Win"],
    ["Mertz", "Skill", "Oddball", "Lucky Seven"],
    ["Frederick", "Skill", "Oddball", "Miracle"],
    ["Marvin", "Skill", "Oddball", "Tip the Scales"],
    ["Pinky", "Skill", "Even Temper", "Generosity"],
    ["Hayley", "Skill", "Even Temper", "Will to Win"],
    ["Pip", "Skill", "Even Temper", "Lucky Seven"],
    ["Gregory", "Skill", "Even Temper", "Miracle"],
    ["Croc", "Skill", "Even Temper", "Tip the Scales"],
    ["Leo", "Skill", "Proud Pebble", "Generosity"],
    ["Stripe", "Skill", "Proud Pebble", "Will to Win"],
    ["Julie B.", "Skill", "Proud Pebble", "Lucky Seven"],
    ["Raito", "Skill", "Proud Pebble", "Miracle"],
    ["Ally", "Skill", "Proud Pebble", "Tip the Scales"],
    ["Bloshi", "Skill", "Pity Pebble", "Generosity"],
    ["Osh", "Skill", "Pity Pebble", "Will to Win"],
    ["Moshi", "Skill", "Pity Pebble", "Lucky Seven"],
    ["Bloshi Jr.", "Skill", "Pity Pebble", "Miracle"],
    ["Ally Jr.", "Skill", "Pity Pebble", "Tip the Scales"],
    ["Shell", "Skill", "Untouchable", "Generosity"],
    ["Taro", "Skill", "Untouchable", "Will to Win"],
    ["Berry", "Skill", "Untouchable", "Lucky Seven"],
    ["Aurora", "Skill", "Untouchable", "Miracle"],
    ["Waddles", "Skill", "Untouchable", "Tip the Scales"],
    ["Juan", "Power", "Oddball", "Generosity"],
    ["Spencer", "Power", "Oddball", "Will to Win"],
    ["Bert", "Power", "Oddball", "Lucky Seven"],
    ["Pete", "Power", "Oddball", "Miracle"],
    ["Cuddlez", "Power", "Oddball", "Tip the Scales"],
    ["Nut", "Power", "Even Temper", "Generosity"],
    ["Ruby", "Power", "Even Temper", "Will to Win"],
    ["Cream", "Power", "Even Temper", "Lucky Seven"],
    ["Flapper", "Power", "Even Temper", "Miracle"],
    ["Bumper", "Power", "Even Temper", "Tip the Scales"],
    ["Wasabi", "Power", "Proud Pebble", "Generosity"],
    ["Chad", "Power", "Proud Pebble", "Will to Win"],
    ["Beefcake", "Power", "Proud Pebble", "Lucky Seven"],
    ["Ima Reddy", "Power", "Proud Pebble", "Miracle"],
    ["Chaucer", "Power", "Proud Pebble", "Tip the Scales"],
    ["Ruth", "Power", "Pity Pebble", "Generosity"],
    ["Luke", "Power", "Pity Pebble", "Will to Win"],
    ["Watson", "Power", "Pity Pebble", "Lucky Seven"],
    ["Dominic Bluey", "Power", "Pity Pebble", "Miracle"],
    ["Almond", "Power", "Pity Pebble", "Tip the Scales"],
    ["Duncan", "Power", "Untouchable", "Generosity"],
    ["Felix", "Power", "Untouchable", "Will to Win"],
    ["Ignatius", "Power", "Untouchable", "Lucky Seven"],
    ["Nickelby", "Power", "Untouchable", "Miracle"],
    ["Grumps", "Power", "Untouchable", "Tip the Scales"],
    ["Dave", "Speed", "Oddball", "Generosity"],
    ["Bonez", "Speed", "Oddball", "Will to Win"],
    ["Simon", "Speed", "Oddball", "Lucky Seven"],
    ["Tom", "Speed", "Oddball", "Miracle"],
    ["Stewart", "Speed", "Oddball", "Tip the Scales"],
    ["Tony", "Speed", "Even Temper", "Generosity"],
    ["Daffy", "Speed", "Even Temper", "Will to Win"],
    ["Carrotz", "Speed", "Even Temper", "Lucky Seven"],
    ["Pabu", "Speed", "Even Temper", "Miracle"],
    ["Barry", "Speed", "Even Temper", "Tip the Scales"],
    ["Duke", "Speed", "Proud Pebble", "Generosity"],
    ["Marcel", "Speed", "Proud Pebble", "Will to Win"],
    ["Spot", "Speed", "Proud Pebble", "Lucky Seven"],
    ["Timmy", "Speed", "Proud Pebble", "Miracle"],
    ["Doug", "Speed", "Proud Pebble", "Tip the Scales"],
    ["Glad", "Speed", "Pity Pebble", "Generosity"],
    ["Brad", "Speed", "Pity Pebble", "Will to Win"],
    ["Yoad", "Speed", "Pity Pebble", "Lucky Seven"],
    ["Bload", "Speed", "Pity Pebble", "Miracle"],
    ["Road", "Speed", "Pity Pebble", "Tip the Scales"],
    ["Pigion", "Speed", "Untouchable", "Generosity"],
    ["Jolly", "Speed", "Untouchable", "Will to Win"],
    ["Shortstop", "Speed", "Untouchable", "Lucky Seven"],
    ["Chalk", "Speed", "Untouchable", "Miracle"],
    ["Buzz", "Speed", "Untouchable", "Tip the Scales"],
]

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

# Create a one indexed schedule for the next month
def generate_schedule():
    left = []
    right = []
    pebblers = pebblers_per_div
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