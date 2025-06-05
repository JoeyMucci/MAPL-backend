from rest_framework import serializers
from .models import *

class PebblerRank(serializers.ModelSerializer):
    class Meta:
        model = Pebbler
        fields = ['name', 'current_rank']

class PebblerBasic(serializers.ModelSerializer):
    class Meta:
        model = Pebbler
        fields = ['name', 'current_rank', 'current_division', 'pebbles', 'home_pebbles', 'away_pebbles', 'qp', 'at']

class PebblerPersonal(serializers.ModelSerializer):
    class Meta:
        model = Pebbler
        fields = ['description', 'trait', 'quirk', 'ability']

class PebblerDivisionSummary(serializers.ModelSerializer):
    class Meta:
        model = Pebbler
        fields = ['masters', 'all_stars', 'professionals', 'learners']

class BoutSmall(serializers.ModelSerializer):
    away = PebblerRank(read_only=True)
    home = PebblerRank(read_only=True)

    class Meta:
        model = Bout
        fields = [
            'away',
            'home',
            'division',
            'time',
            'away_quirk',
            'home_quirk',
            'away_ability',
            'home_ability',
            'away_roll_final',
            'home_roll_final',
            'away_score',
            'home_score',
        ]

class PerformanceMain(serializers.ModelSerializer):
    pebbler = serializers.StringRelatedField()

    class Meta:
        model = Performance 
        fields = [
                'pebbler',
                'pebbles',
                'played', 
                'wins',
                'ties', 
                'losses', 
                'pf', 
                'pa', 
                'pd', 
                'away_played', 
                'home_played', 
                'away_pebbles', 
                'home_pebbles', 
                'qp', 
                'form', 
                'rank', 
                'previous_rank', 
        ]   

class PerformanceSummary(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = [
            'pebbles',
            'rank',
            'division',
            'month',
            'year',
        ]