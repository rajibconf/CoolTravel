"""API > serializers > district.py"""
from rest_framework import serializers
from coolapp.models import District


class DistrictSerializer(serializers.ModelSerializer):
    # Define an additional field for 'average_temperature_2pm'
    average_temperature_2pm = serializers.FloatField()

    class Meta:
        model = District
        fields = [
            'id', 'name', 'bn_name', 'lat',
            'long', 'average_temperature_2pm'
        ]
