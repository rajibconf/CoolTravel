"""coolapp > models > temperature.py"""
# DJANGO IMPORTS
from django.db import models
from django.utils.translation import gettext_lazy as _
# APP IMPORTS
from coolapp.models import District

    
class TemperatureData(models.Model):
    """TemperatureData model"""
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    average_temperature_2pm = models.DecimalField(max_digits=5, decimal_places=1)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    last_updated = models.DateTimeField(_('Last Updated'))
    
    class Meta:
        verbose_name = _('Temperature Data')
        indexes = [
            models.Index(fields=['district', 'average_temperature_2pm'])
            ]

    def __str__(self):
        return str(self.district)


class TemperatureForecast(models.Model):
    """TemperatureForecast model"""
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    generationtime_ms = models.FloatField()
    utc_offset_seconds = models.IntegerField()
    timezone = models.CharField(max_length=255)
    timezone_abbreviation = models.CharField(max_length=10)
    elevation = models.FloatField()
    hourly_units_time = models.CharField(max_length=255)
    hourly_units_temperature_2m = models.CharField(max_length=10)
    hourly_time = models.JSONField()
    hourly_temperature_2m = models.JSONField()
    
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    last_updated = models.DateTimeField(_('Last Updated'))
    is_active = models.BooleanField(_('Is Active'), default=True)
    

    def __str__(self):
        return f"Temperature Forecast for Latitude: {self.latitude}, Longitude: {self.longitude}"
