from django.db import models

class Pebbler(models.Model):
    name = models.CharField(max_length=20)

    pebbles = models.IntegerField(default=0)

    current_rank = models.IntegerField(null=True)

    description = models.CharField(max_length=128)
    isMale = models.BooleanField()

    # Grace, Skill, Power, Speed
    trait = models.CharField(max_length=5)

    # Oddball, Even Temper, Proud Pebble, Pity Pebble, Untouchable
    quirk = models.CharField(max_length=12)

    # Generosity, Will to Win, Lucky Seven, Miracle, Tip the Scales
    ability = models.TextField(max_length=14)

    away_pebbles = models.IntegerField(default=0)
    home_pebbles = models.IntegerField(default=0)
    qp = models.IntegerField(default=0)
    at = models.IntegerField(default=0)

    # Master, All-Star, Professional, Learner 
    current_division = models.CharField(max_length=12)

    masters = models.IntegerField(default=0)
    all_stars = models.IntegerField(default=0)
    professionals = models.IntegerField(default=0)
    learners = models.IntegerField(default=0)

    # Year To Date
    ytd_pebbles = models.IntegerField(default=0)
    ytd_away_pebbles = models.IntegerField(default=0)
    ytd_home_pebbles = models.IntegerField(default=0)
    ytd_qp = models.IntegerField(default=0)
    ytd_at = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Bout(models.Model):
    away = models.ForeignKey(Pebbler, on_delete=models.CASCADE, related_name='away_bouts')
    home = models.ForeignKey(Pebbler, on_delete=models.CASCADE, related_name='home_bouts')

    time = models.DateTimeField()

    # Master, All-Star, Professional, Learner 
    division = models.CharField(max_length=12)

    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()

    away_roll = models.IntegerField(null=True)
    home_roll = models.IntegerField(null=True)
    away_quirk = models.BooleanField(default=False)
    home_quirk = models.BooleanField(default=False)
    away_ability = models.BooleanField(default=False)
    home_ability = models.BooleanField(default=False)
    away_roll_half = models.IntegerField(null=True)
    home_roll_half = models.IntegerField(null=True)
    away_roll_final = models.IntegerField(null=True)
    home_roll_final = models.IntegerField(null=True)
    away_score = models.IntegerField(default=0)
    home_score = models.IntegerField(default=0)

    last_in_day = models.BooleanField()

    def __str__(self):
        return f"{self.division}: {self.away} @ {self.home} ({self.month:02d}-{self.day:02d}-{self.year})"

class Performance(models.Model):
    pebbler = models.ForeignKey(Pebbler, on_delete=models.CASCADE, related_name='performances')

    pebbles = models.IntegerField(default=0)

    # Master, All-Star, Professional, Learner 
    division = models.CharField(max_length=1)

    year = models.IntegerField()
    month = models.IntegerField()

    played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    ties = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    pf = models.IntegerField(default=0)
    pa = models.IntegerField(default=0)
    pd = models.IntegerField(default=0)

    away_played = models.IntegerField(default=0)
    home_played = models.IntegerField(default=0)
    away_pebbles = models.IntegerField(default=0)
    home_pebbles = models.IntegerField(default=0)

    qp = models.IntegerField(default=0)
    at = models.IntegerField(default=0)

    form = models.CharField(max_length=30, default="")

    rank = models.IntegerField()
    previous_rank = models.IntegerField()
    tiebreaker = models.IntegerField()

    def __str__(self):
        return f"{self.division}: {self.pebbler} ({self.year}-{self.month:02d})"
