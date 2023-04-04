from rest_framework import serializers

from demo.models import Temperature, ScannerTemperature


class ScannerTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScannerTemperature
        fields = "__all__"


class TemperatureSerializer(serializers.ModelSerializer):
    scanner = ScannerTemperatureSerializer(many=False)

    class Meta:
        model = Temperature
        fields = "__all__"


class PostTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = "__all__"
