"""API > views > __init__.py"""
from .token import ObtainTokenView, LogoutView
from .cool_district import CoolestDistricts, TravelRecommendation
# update the following list to allow classes to be available for import
# this is very useful especially when using from .file import *
__all__ = [
    ObtainTokenView, LogoutView, CoolestDistricts, TravelRecommendation
]
