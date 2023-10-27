"""coolapp > models > distrcit.py"""
# DJANGO IMPORTS
from django.db import models
from django.utils.translation import gettext_lazy as _


class District(models.Model):
    """District model"""
    division_id = models.CharField(max_length=10)
    name = models.CharField(_('Name'), max_length=100)
    bn_name = models.CharField(_('Bangla Name'), max_length=100)
    lat = models.CharField(_('Latitude'), max_length=20)
    long = models.CharField(_('Longitude'), max_length=20)
    is_active = models.BooleanField(
        _('Is Active'), default=True
    )
    created_at = models.DateTimeField(
        _('Created At'), auto_now_add=True, null=True
    )
    last_updated = models.DateTimeField(
        _('Last Updated'), auto_now=True, null=True
    )
    
    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')
        indexes = [
            models.Index(fields=['name', 'bn_name', 'lat', 'long'])
            ]

    def __str__(self):
        return self.name