"""coolapp > models > temperature.py"""
# DJANGO IMPORTS
from django.db import models
from django.utils.translation import gettext_lazy as _
# APP IMPORTS
from coolapp.models import District

    
class TemperatureData(models.Model):
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
