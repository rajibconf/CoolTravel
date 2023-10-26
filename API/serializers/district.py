"""API > serializers > district.py"""
from rest_framework import serializers
from coolapp.models import District

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'  # This includes all fields in the serialization
