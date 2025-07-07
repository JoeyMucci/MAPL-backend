from rest_framework import serializers
from .models import *

class PebblerName(serializers.ModelSerializer):
    class Meta:
        model = Pebbler
        fields = ['name']

class PebblerBasic(serializers.ModelSerializer):
    class Meta:
        model = Pebbler
        fields = [
            'name', 
            'current_rank', 
            'current_division', 
            'pebbles', 
            'home_pebbles', 
            'away_pebbles', 
            'qp', 
            'at', 
            'ytd_pebbles', 
            'ytd_home_pebbles', 
            'ytd_away_pebbles', 
            'ytd_qp', 
            'ytd_at', 
            'masters', 
            'all_stars', 
            'professionals', 
            'learners',
        ]

class PebblerPersonal(serializers.ModelSerializer):
    class Meta:
        model = Pebbler
        fields = ['name', 'description', 'trait', 'quirk', 'ability']

class BoutSmall(serializers.ModelSerializer):
    away = PebblerName(read_only=True)
    home = PebblerName(read_only=True)

    class Meta:
        model = Bout
        fields = [
            'id',
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

class BoutFull(serializers.ModelSerializer):
    away = PebblerPersonal(read_only=True)
    home = PebblerPersonal(read_only=True)

    class Meta:
        model = Bout
        exclude = ['time', 'last_in_day']

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