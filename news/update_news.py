# This code is intended to be run as a standalone script or as part of a scheduled task.
# It will automatically generate a report for the given day's bouts and create it in the database

import anthropic
from league.models import *
from news.models import *
from news.serializers import *
from django.utils import timezone
import datetime
import os

PROMOTE_DEMOTE_THRESHOLD = 13
FINAL_DAY = 25
BOUTS_IN_DAY = 48

real_time = False
y = 2025
m = 9
d = 1

sys_prompts = {
    "Ari" : "You are Ari, a passionate octopus. In your response, you should employ an excited and optimistic tone for what is coming next.",
    "Patrick" : "You are Patrick, a scholarly bear. In your response, you should use flowery language as you analyze the bouts.",
    "Lippo" : "You are Lippo, a boisterous parrot. In your response, you should employ an absurd tone and repeat things for emphasis, such as high pebble earnings and long streaks.",
}

reporters = Reporter.objects.all()

if len(reporters) == 0:
    lippo = Reporter(
        name = "Lippo",
        description = '''An incredulous parrot and boisterous reporter. Often repeats details that are particularly amazing 
        in his reporting. Some have speculated that he is related to a certain pebbler, although no one can say for sure.'''
    )

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
    
    Reporter.objects.bulk_create([lippo, ari, patrick])


if real_time:
    cur_time = timezone.now()
    y = cur_time.year
    m = cur_time.month
    d = cur_time.day

reports = Report.objects.all().filter(year=y, month=m, day=d)
bouts = Bout.objects.filter(month=m, day=d, year=y, away_roll__isnull=False)

if len(reports) == 0 and len(bouts) == BOUTS_IN_DAY:
    day_of_week = datetime.date(y, m, d).strftime('%A')

    serializer = BoutFull(bouts, many=True)

    for bout in serializer.data:
        for side in ["away", "home"]:
            change = bout[side]["performances"][0]["previous_rank"] - bout[side]["performances"][0]["rank"]

            if change < 0:
                bout[side]["performances"][0]["ranking_change"] = "Down " + str(abs(change)) + " spot" + ("s" if abs(change) > 1 else "")
            elif change > 0:
                bout[side]["performances"][0]["ranking_change"] = "Up " + str(abs(change)) + " spot" + ("s" if abs(change) > 1 else "")
            else:
                bout[side]["performances"][0]["ranking_change"] = "Rank stays the same"

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

    league_results = {
        "month": m, 
        "day": d, 
        "year": y, 
        "bouts": serializer.data
    }

    author = "Ari"

    if day_of_week == "Tuesday" or day_of_week == "Thursday":
        author = "Patrick"
    elif day_of_week == "Saturday" or day_of_week == "Sunday":
        author = "Lippo"

    final_instruction = ""

    if d >= PROMOTE_DEMOTE_THRESHOLD:
        final_instruction = "7. Mention each pebbler's standing with regards to promotion/demotion"
    
    if d == FINAL_DAY:
        final_instruction = "7. Mention whether each pebbler got promoted, demoted, or stayed in the same division"

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
                    Generosity: If tied with opponent, double tie bonus
                    Will to Win: If tied with opponent, reroll and double win bonus
                    Tip the Scales: If trailing by one, switch rolls with opponent

                    Here is the data containing the league results for today.

                    {league_results}

                    Your task is to create a report meant to be read in print. As such, only include words in the voice of {author}.

                    Report on a bout if and only if it meets at least one of the following conditions:
                    1. At least one pebbler triggered their ability
                    2. Each pebbler is named in the other's description
                    3. Both pebblers are members of the same group (tell from description)
                    3. Both pebblers in the bout were in ranks 1-5 before the bout (previous_rank)
                    4. Both pebblers in the bout are in ranks 21-25 before the bout (previous_rank)
                    5. If there are less than 3 bouts that meet the conditions, pick random bouts to reach at least 3.

                    Report on bouts in this format:
                    1. Mention the initial rolls
                    2. Mention any quirk activations
                    3. Mention any ability triggers, including what the outcome of the ability was, in the order they occurred
                    4. Mention how many pebbles each pebbler earned independently
                    5. Mention any streaks that each pebbler extended or snapped.
                    6. Mention how each pebbler's ranking changed.
                    {final_instruction}

                    Your response should be in this format:
                    1. Brief introductory paragraph
                    2. Paragraph for each bout
                    3. Brief conclusion paragraph 
                    '''
            }
        ],
    )

    title = ""
    essay = ""

    if response.type == "message":
        for block in response.content:
            if block.type == "text":
                essay = block.text

                response = anthropic.Anthropic().messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=20000,
                    system=sys_prompts[author].split('.')[0],
                    messages=[
                        {"role": "user", "content":
                            f"""
                            Create a creative 10-20 word title for the following article.

                            {essay}
                            """
                         }
                    ],
                )

                if response.type == "message":
                    for block in response.content:
                        if block.type == "text":
                            title = block.text
                            Report.objects.create(
                                author = Reporter.objects.get(name=author),
                                year = y,
                                month = m,
                                day = d,
                                content = essay,
                                title = title,
                            )
