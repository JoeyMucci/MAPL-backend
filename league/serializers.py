from rest_framework import serializers
from .models import *

class PebblerFull(serializers.ModelSerializer):
    class Meta:
        model = Pebbler
        fields = '__all__'

class PebblerPreview(serializers.ModelSerializer):
    class Meta:
        model = Pebbler
        fields = ['name', 'current_rank']

class BoutPreview(serializers.ModelSerializer):
    away = PebblerPreview(read_only=True)
    home = PebblerPreview(read_only=True)

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

    