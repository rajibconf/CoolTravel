"""API > serializers > user.py"""
# DJANGO IMPORTS
from django.contrib.auth import get_user_model
# DRF IMPORTS
from rest_framework import serializers

USER_MODEL = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User and Profile models"""

    class Meta:
        """Meta class"""
        model = USER_MODEL
        fields = [
            'id', 'email', 'last_login', 'is_active',
            'is_staff', 'is_superuser'
            ]
        read_only_fields = (
            'last_login', 'is_active', 'is_staff', 'is_superuser',
        )