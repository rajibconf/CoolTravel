"""API > urls.py"""
# DJANGO IMPORTS
from django.urls import path, include
# DRF IMPORTS
from rest_framework.routers import DefaultRouter
# API IMPORTS
from API import views


# /api/... browsable drf api
app_name = 'api'

# https://www.django-rest-framework.org/api-guide/routers/
router = DefaultRouter()

# https://docs.djangoproject.com/en/3.1/topics/http/urls/
urlpatterns = [
    # auth --------------------------------------------------------------------
    path('auth/login/', views.ObtainTokenView.as_view(), name='auth-login'),
    path('auth/logout/', views.LogoutView.as_view(), name='auth-logout'),
    
    # auth --------------------------------------------------------------------
    path('cool-district/', views.CoolestDistricts.as_view(), name='cool-district'),

    # router ------------------------------------------------------------------
    path('', include(router.urls)),
]
