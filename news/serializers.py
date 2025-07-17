from rest_framework import serializers
from league.models import *
from news.models import *

class ReporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporter
        fields = ["description"]

class ReportSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Report
        fields = ["author", "title", "content", "id", "month", "day", "year"]

class PebblerFull(serializers.ModelSerializer):
    performances = serializers.SerializerMethodField()

    def get_performances(self, obj):
        perf = obj.performances.order_by('-year', '-month').first()
        if perf:
            return [{
                "form": perf.form,
                "rank": perf.rank,
                "previous_rank": perf.previous_rank,
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
        exclude = ['id', 'time', 'last_in_day']
