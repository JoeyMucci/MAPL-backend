# This code is intended to be run as a standalone script or as part of a scheduled task.
# It will automatically generate a report for the given day's bouts and create it in the database

import anthropic
from league.models import *
from news.models import *
from news.serializers import *
from news.views import get_claude_data
from django.utils import timezone
import datetime
import os
import re

RANKINGS_THRESHOLD = 3
PROMOTE_DEMOTE_THRESHOLD = 13
FINAL_DAY = 25
BOUTS_IN_DAY = 48

real_time = True
y = 2025
m = 13
d = 1

if real_time:
    cur_time = timezone.now()
    y = cur_time.year
    m = cur_time.month
    d = cur_time.day

sys_prompts = {
    "Ari" : "You are Ari, a passionate octopus. In your response, you should employ an optimistic tone for what is coming next.",
    "Patrick" : "You are Patrick, a scholarly bear. In your response, you should use flowery language as you analyze the bouts.",
    "Lippo" : "You are Lippo, a boisterous parrot. In your response, you should employ an absurd tone and repeat things for emphasis, such as high pebble earnings.",
}

reporters = Reporter.objects.all()

if len(reporters) == 0:
    ari = Reporter(
        name = "Ari",
        description = '''An octopus mother and industrious reporter. Is motivated to always get the scoop on the latest happenings 
        in the MAPL. Once held a pessimistic world view, but had a change of heart thanks to encounters with a kind soul.'''
    )

    patrick = Reporter(
        name = "Patrick",
        description = '''A scholarly bear and detailed reporter. Likes to use his extensive vocabulary and deep knowledge of 
        the pebblers while reporting. In his free time, enjoys following or curating competitions of all varieties.'''
    )

    lippo = Reporter(
        name = "Lippo",
        description = '''An incredulous parrot and boisterous reporter. Often repeats details that are particularly amazing 
        in his reporting. Some have speculated that he is related to a certain pebbler, although no one can say for sure.'''
    )
    
    Reporter.objects.bulk_create([ari, patrick, lippo])

referees = Referee.objects.all()

if len(referees) == 0:
    shaun = Referee(
        name = "Shaun",
        description = '''A shy guy and an inconspicuous referee. Overcomes his timid nature to educate on the rules of the MAPL and go on 
        various adventures. Some of his past exploits include kart racing, game show hosting, and amateur athletics.'''
    )

    neville = Referee(
        name = "Neville",
        description = '''An airborne turtle and a strict referee. Enforces the rules of the MAPL expertly, understanding every nuance
        of how bouts are carried out. Throws spiky red objects whenever he needs to interject and make a ruling.'''
    )

    tickle = Referee(
        name = "Tickle",
        description = '''A walking time bomb and a concise referee. Excels at keeping things moving when on the job, communicating
        quickly and effectively. Is suprisingly laid back after his work is done.'''
    )

    Referee.objects.bulk_create([shaun, neville, tickle])

reports = Report.objects.all().filter(year=y, month=m, day=d)
bouts = Bout.objects.filter(month=m, day=d, year=y, away_roll__isnull=False)

if len(reports) == 0 and len(bouts) == BOUTS_IN_DAY:
    bouts_to_report = get_claude_data(bouts, d)

    league_results = {
        "month": m, 
        "day": d, 
        "year": y, 
        "bouts": bouts_to_report
    }

    author = "Ari"
    day_of_week = datetime.date(y, m, d).strftime('%A')

    if day_of_week == "Tuesday" or day_of_week == "Thursday":
        author = "Patrick"
    elif day_of_week == "Saturday" or day_of_week == "Sunday":
        author = "Lippo"

    writing_points = [
        "-  Mention the division of the bout"
        "-  Mention the pebblers competing, noting any notable circumstances"
        "-  Mention the initial rolls",
        "-  Mention any quirk activations",
        "-  Mention any ability triggers, including what the outcome of the ability was, in the order they occurred",
        "-  Mention how many pebbles each pebbler earned independently",
    ]

    if d >= RANKINGS_THRESHOLD:
        writing_points.append("-  Mention any streaks that each pebbler extended or snapped")
        writing_points.append("-  Mention how each pebbler's ranking changed")

    if d == FINAL_DAY:
        writing_points.append("-  Mention whether each pebbler got promoted, demoted, or stayed in the same division")
    elif d >= PROMOTE_DEMOTE_THRESHOLD:
        writing_points.append("-  Mention each pebbler's standing with regards to promotion/demotion")

    api_key = os.environ.get("ANTHROPIC_API_KEY")

    client = anthropic.Anthropic(
        api_key=api_key
    )

    date_str = datetime.date(y, m, d).strftime('%B %d, %Y').replace(' 0', ' ')
    msg = f'''
The Mega Auto Pebble League (MAPL) is a perpetual competition between 100 competitors referred to as "pebblers".

At any given time, there are 25 pebblers in each of 4 divisions.
The 4 divisions listed from highest to lowest are:
    Master 
    All-Star 
    Professional 
    Learner
    
Competition occurs in cycles that run from the 1st to the 25th of each month. 
During the competition cycle, pebblers compete against one another to accumulate pebbles.
Pebblers are ranked on the number of pebbles they accumulate.
At the end of the cycle, the top 5 pebblers are promoted to the next higher division and the bottom 5 pebblers are demoted to the next lower division.
*Note that in the Master division, promotion is impossible because there is no division higher than Master.
*Note that in the Learner division, demotion is impossible because there is no division lower than Learner.

Each encounter between two pebblers is called a bout. Bouts follow this process:
-  Both pebblers roll according to their trait
-  Quirks may activate and grant pebblers instant pebbles to add to their total
-  The away pebbler may trigger their ability causing the rolls to change
-  Halftime
-  The home pebbler may trigger their ability causing the rolls to change
-  Pebbles are awarded based on the final rolls

Below is useful context for reporting on the bouts: 

    The formula for calculating base pebbles is broken down by result:
        Higher roll: <roll difference> + 3; 3 is the "win bonus"
        Lower roll: 0
        Same roll: 2; 2 is the "tie bonus"
        *Note that a pebbler can increase the value of their "win bonus" or "tie bonus" without affecting its value for the other pebbler. 

    Traits dictate initial rolls:
        Grace: 1, 2, 4, 4, 5, 5
        Skill: 1, 3, 3, 4, 4, 6
        Power: 1, 1, 2, 5, 5, 6
        Speed: 1, 1, 3, 3, 6, 6

    Quirks grant 1-2 instant pebbles after the initial rolls if the appropriate condition is met:
        Pity Pebble: Trailing by two or more
        Proud Pebble: Leading by two or more
        Oddball: Roll parity differs from day parity and opponent roll parity
        Even Temper: Roll parity matches day parity and opponent roll parity
        Untouchable: Opponent roll is one

    Abilities may trigger when a condition is met to dramatically change bouts:
        Miracle: Trailing opponent -> Upgrade your roll to opponent's roll
        Lucky Seven: Leading opponent -> Upgrade your roll to 7
        Generosity: Tying opponent -> Double your tie bonus
        Will to Win: Tying opponent -> Reroll and double your win bonus
        Tip the Scales: Trailing by exactly 1 -> Switch your roll with opponent's roll

    The formula for calculating final pebbles is <quirk pebbles> + 3 * <base pebbles>

Here is the data containing notable bout results for {date_str}:

{league_results}

Your task is to create a report meant to be read in print. As such, only include words in the voice of {author}.

Report on bouts according to the following format:
{'\n'.join(writing_points)}

Your response should be in this format:
-  Brief introductory paragraph
-  Paragraph for each bout
-  Brief conclusion paragraph

Be sure to mention every bout.

Before submitting, filter out your response for any content that is not part of the report. 
'''
    
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
                "content": msg
            }
        ],
    )

    title = ""
    essay = ""

    if response.type == "message":
        for block in response.content:
            if block.type == "text":
                essay = block.text
                essay = re.sub(r"(?m)^\s*\*\*.+?\*\*\s*:?\s*", "", essay)
                essay = essay.strip()

                response = anthropic.Anthropic().messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=20000,
                    system=sys_prompts[author].split('.')[0],
                    messages=[
                        {"role": "user", "content":
                            f"""
Create a creative 10-20 word title for the following article:

{essay}

Before submitting, filter out your response for any content that is not part of the title. 
"""
                         }
                    ],
                )

                if response.type == "message":
                    for block in response.content:
                        if block.type == "text":
                            title = block.text
                            if title[0] == "\"" and title[-1] == "\"":
                                title = title[1:-1]
                            if title[:2] == "**" and title[-2:] == "**":
                                title = title[2:-2]
                            if title[0] == "\"" and title[-1] == "\"":
                                title = title[1:-1]
                            Report.objects.create(
                                author = Reporter.objects.get(name=author),
                                year = y,
                                month = m,
                                day = d,
                                content = essay,
                                title = title,
                            )
