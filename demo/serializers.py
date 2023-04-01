from rest_framework import serializers

from demo.models import Temperature


class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = "__all__"
