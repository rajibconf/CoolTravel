"""site_settings > models > admin.py"""
# DJANGO IMPORTS
from django.contrib import admin
# APP IMPORTS
from coolapp import models


@admin.register(models.District)
class DistrictModelAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'bn_name',
        'lat', 'long', 'is_active'
    ]
    search_fields = ['name', 'bn_name']
    readonly_fields = ('created_at', 'last_updated')
    list_filter = ['is_active']


@admin.register(models.TemperatureData)
class TemperatureDataModelAdmin(admin.ModelAdmin):
    list_display = [
        'district', 'average_temperature_2pm',
        'created_at', 'last_updated'
    ]
    search_fields = ['name', 'bn_name']
    readonly_fields = ('created_at', 'last_updated')
    ordering = ('average_temperature_2pm', )


@admin.register(models.TemperatureForecast)
class TemperatureForecastModelAdmin(admin.ModelAdmin):
    list_display = [
        'district', 'latitude', 'longitude', 'timezone',
        'travel_date', 'created_at', 'last_updated'
    ]
    search_fields = ['timezone', ]
    readonly_fields = ('created_at', 'last_updated')
    ordering = ('created_at', )
