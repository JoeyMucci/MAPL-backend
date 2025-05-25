from rest_framework import serializers
from .models import *

class BoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bout
        fields = '__all__'