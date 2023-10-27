"""API > views > cool_district.py"""
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from concurrent.futures import ThreadPoolExecutor
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
# APP IMPORTS
from coolapp.models import District, TemperatureData
from coolapp.utils import get_temperature_forecast
from API.serializers import DistrictSerializer


class CoolestDistrictsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CoolestDistricts(ListAPIView):
    serializer_class = DistrictSerializer
    pagination_class = CoolestDistrictsPagination

    def get_queryset(self):
        # Check if the data is cached
        cached_data = cache.get("coolest_districts")

        if cached_data is not None:
            return cached_data

        # Retrieve all districts and their coordinates in a single query
        districts = District.objects.values('id', 'name', 'bn_name', 'lat', 'long')

        def fetch_and_process_district(district):
            try:
                temperature_data = TemperatureData.objects.get(district_id=district['id'])
                if temperature_data.last_updated < timezone.now() - timezone.timedelta(hours=1):
                    # Data is outdated, update it
                    new_temperature_data = get_temperature_forecast(district['lat'], district['long'])
                    average_temperature = round(sum(new_temperature_data[3:10]) / 7, 1) if new_temperature_data else None
                    temperature_data.average_temperature_2pm = average_temperature
                    temperature_data.last_updated = timezone.now()
                    temperature_data.save()
            except TemperatureData.DoesNotExist:
                # Data doesn't exist, create a new entry
                new_temperature_data = get_temperature_forecast(district['lat'], district['long'])
                average_temperature = round(sum(new_temperature_data[3:10]) / 7, 1) if new_temperature_data else None
                temperature_data = TemperatureData(
                    district_id=district['id'],
                    average_temperature_2pm=average_temperature,
                    last_updated=timezone.now()
                )
                temperature_data.save()

            district['average_temperature_2pm'] = temperature_data.average_temperature_2pm
            return district

        with ThreadPoolExecutor() as executor:
            # Use `map` to parallelize the execution of `fetch_and_process_district`
            coolest_districts = list(executor.map(fetch_and_process_district, districts))

        # Sort the list of districts by average temperature (coolest first)
        coolest_districts.sort(key=lambda x: x['average_temperature_2pm'])

        # Cache the data for future requests (with a reasonable expiration time)
        cache.set("coolest_districts", coolest_districts, 3600)  # Cache data for 1 hour

        return coolest_districts
