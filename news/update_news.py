# This code is intended to be run as a standalone script or as part of a scheduled task.
# It will automatically generate a report for the given day's bouts and create it in the database

import anthropic
from league.models import *
from news.models import *
from news.serializers import *
from django.utils import timezone
import datetime
import os

MAX_DAY = 25
PROMOTE_DEMOTE_THRESHOLD = 13

real_time = False
y = 2025
m = 7
d = 13

sys_prompts = {
    "Ori" : "You are Ori, a high energy octopus and mother to a newborn. In your response, you should act like you are a detective trying to get the 'scoop' on what is happening in each bout.",
    "Joey" : "You are Joey, a dignified scholar. In your response, you should treat each pebbler fairly, focusing on their positive traits whenever possible.",
    "Filipo" : "You are Filipo, an incredulous parrot. In your response, you should repeat things for emphasis, particularly things that you cannot believe, such as high pebble earnings.",
}


if real_time:
    cur_time = timezone.now()
    y = cur_time.year
    m = cur_time.month
    d = cur_time.day

reports = Report.objects.all().filter(year=y, month=m, day=d)

if d <= MAX_DAY and len(reports) == 0:
    day_of_week = datetime.date(y, m, d).strftime('%A')
    bouts = Bout.objects.filter(month=m, day=d, year=y)

    serializer = BoutFull(bouts, many=True)

    league_results = {
        "month": m, 
        "day": d, 
        "year": y, 
        "bouts": serializer.data
    }

    author = "Ori"

    if day_of_week == "Tuesday" or day_of_week == "Thursday":
        author = "Joey"
    elif day_of_week == "Saturday" or day_of_week == "Sunday":
        author = "Filipo"

    final_instruction = ""

    if d >= PROMOTE_DEMOTE_THRESHOLD:
        final_instruction = "7. Mention each pebbler's standing with regards to promotion/demotion"


    api_key = os.environ.get("ANTHROPIC_API_KEY")

    client = anthropic.Anthropic(
        api_key=api_key
    )
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=20000,
        system=sys_prompts[author],
        thinking={
            "type": "enabled",
            "budget_tokens": 16000
        },
        messages=[
            {
                "role": "user", 
                "content": 
                    f'''
                    The Mega Automated Pebble League (MAPL) is a perpetual competition between 100 competitors referred to as "pebblers". At any given time, there are 25 pebblers in each of four divisions, which are now listed from most prestigious to least prestigious: "Master", "All-Star", "Professional", "Learner". Competition occurs in cycles that run from the 1st to the 25th of each month. At the end of each cycle, the top 5 pebblers with the most pebbles in each division except Master are promoted (i.e. Professional to All-Star) and the bottom 5 pebblers with the fewest pebbles in each division except Learner are demoted (i.e. Professional to Learner). 

                    Each encounter between two pebblers is called a bout. Bouts follow this process:
                    1. Both pebblers roll according to their trait
                    2. Quirks may activate and grant pebblers instant pebbles to add to their total
                    3. The away pebbler may trigger their ability causing the rolls to change
                    4. Halftime
                    5. The home pebbler may trigger their ability causing the rolls to change
                    6. Pebbles are awarded based on the final rolls

                    Here is a list of what the abilities do:
                    Miracle: If trailing opponent, upgrade roll to opponent's roll
                    Lucky Seven: If leading opponent, upgrade roll to 7
                    Generosity: If tied with opponent, double draw bonus
                    Will to Win: If tied with opponent, reroll and double win bonus
                    Tip the Scales: If trailing by one, switch rolls with opponent

                    Here is the data containing the league results for today.

                    {league_results}

                    Report on a bout if and only if it meets at least one of the following conditions:
                    1. At least one pebbler triggered their ability
                    2. Each pebbler is named in the other's description
                    3. Both pebblers are members of the same group (tell from description)
                    3. Both pebblers in the bout were in ranks 1-5 before the bout (previous_rank)
                    4. Both pebblers in the bout are in ranks 21-25 before the bout (previous_rank)

                    Report on bouts in this fashion:
                    1. Mention the initial rolls
                    2. Mention any quirk activations
                    3. Mention any ability triggers, including what the outcome of the ability was, in the order they occurred
                    4. Mention how many pebbles each pebbler earned independently
                    5. Mention if any pebbler extended or snapped a win/loss streak of more than 3 in a row (look at form string, each character represents a win, tie, or loss. Note that today's results have already been appended to the end of the string)
                    6. Mention how each pebbler's ranking changed. (from previous_rank to rank)
                    {final_instruction}

                    Your response should be a text description (no bullet points) for each bout. Each bout description should be its own paragraph. No introductory or concluding paragraphs. You are familiar with the rules and your audience is as well, so you can exclude details on how the ability works but do remember to explain what they did in the context of the bout. 
                    '''
            }
        ],
    )

    if response.type == "message":
        for block in response.content:
            if block.type == "text":
                Report.objects.create(
                    author = Reporter.objects.get(name=author),
                    year = y,
                    month = m,
                    day = d,
                    content = block.text,
                )
