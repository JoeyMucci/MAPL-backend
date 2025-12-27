from rest_framework import serializers
from league.models import *
from news.models import *

class ReporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporter
        fields = ["description", "name"]

class SmallReportSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Report
        fields = ["author", "title", "id", "month", "day", "year"]

class FullReportSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Report
        fields = ["author", "title", "content", "id", "month", "day", "year"]

class PebblerFull(serializers.ModelSerializer):
    performances = serializers.SerializerMethodField()

    def get_performances(self, obj):
        perfs = obj.performances.order_by('-year', '-month')
        if perfs:
            if len(perfs[0].form) > 0:
                return [{
                    "form": perfs[0].form,
                    "rank": perfs[0].rank,
                    "previous_rank": perfs[0].previous_rank,
                }]
            elif len(perfs) > 1 and len(perfs[1].form) > 0:
                return [{
                    "form": perfs[1].form,
                    "rank": perfs[1].rank,
                    "previous_rank": perfs[1].previous_rank,
                }]
        return []

    class Meta:
        model = Pebbler
        fields = [
            'name', 
            'description', 
            'isMale',
            'trait', 
            'quirk', 
            'ability', 
            'performances',
        ]

class BoutFull(serializers.ModelSerializer):
    away = PebblerFull(read_only=True)
    home = PebblerFull(read_only=True)

    class Meta:
        model = Bout
        exclude = ['id', 'last_in_day']
