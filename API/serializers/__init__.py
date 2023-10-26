"""API > serializers > __init__.py"""
from .user import UserSerializer
from .token import TokenSerializer, LogoutSerializer
from .district import DistrictSerializer

# update the following list to allow classes to be available for import
# this is very useful especially when using from .file import *
__all__ = [
    UserSerializer, TokenSerializer,
    LogoutSerializer, DistrictSerializer
]
