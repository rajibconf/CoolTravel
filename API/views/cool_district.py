"""API > views > cool_district.py"""
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from concurrent.futures import ThreadPoolExecutor
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
# APP IMPORTS
from coolapp.models import District, TemperatureData, TemperatureForecast
from coolapp.utils import get_temperature_forecast, get_temperature_forecast_raw
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



class TravelRecommendation(APIView):
    
    def post(self, request):
        source_location = request.query_params.get("source_location")
        destination_location = request.query_params.get("destination_location")
        travel_date = request.query_params.get("travel_date")
        missing_parameters = []
        if source_location is None:
            missing_parameters.append("source_location")
        if destination_location is None:
            missing_parameters.append("destination_location")
        if travel_date is None:
            missing_parameters.append("travel_date")
        if missing_parameters:
            return Response({"error": f"Missing required parameters: {', '.join(missing_parameters)}"}, status=400)

        
        # Retrieve all districts and their coordinates in a single query
        districts = District.objects.filter(Q(name__iexact=source_location) | Q(name__iexact=destination_location)).values('id', 'name', 'bn_name', 'lat', 'long')

        def fetch_and_process_district(district):
            try:
                temperature_data = TemperatureForecast.objects.get(district_id=district['id'])
                if temperature_data.last_updated < timezone.now() - timezone.timedelta(hours=1):
                    # Data is outdated, update it
                    data_dict = get_temperature_forecast_raw(district['lat'], district['long'])
                    temperature_data.generationtime_ms = data_dict['generationtime_ms']
                    temperature_data.hourly_time = data_dict["hourly"]["time"]
                    temperature_data.hourly_temperature_2m = data_dict["hourly"]["temperature_2m"]
                    temperature_data.last_updated = timezone.now()
                    temperature_data.save()
            except TemperatureForecast.DoesNotExist:
                # Data doesn't exist, create a new entry
                data_dict = get_temperature_forecast_raw(district['lat'], district['long'])
                forecast = TemperatureForecast(
                    district_id=district['id'],
                    latitude=data_dict["latitude"],
                    longitude=data_dict["longitude"],
                    generationtime_ms=data_dict["generationtime_ms"],
                    utc_offset_seconds=data_dict["utc_offset_seconds"],
                    timezone=data_dict["timezone"],
                    timezone_abbreviation=data_dict["timezone_abbreviation"],
                    elevation=data_dict["elevation"],
                    hourly_units_time=data_dict["hourly_units"]["time"],
                    hourly_units_temperature_2m=data_dict["hourly_units"]["temperature_2m"],
                    hourly_time=data_dict["hourly"]["time"],
                    hourly_temperature_2m=data_dict["hourly"]["temperature_2m"],
                    last_updated=timezone.now()
                )
                # Save the instance to the database
                forecast.save()
            return district

        with ThreadPoolExecutor() as executor:
            # Use `map` to parallelize the execution of `fetch_and_process_district`
            coolest_districts = list(executor.map(fetch_and_process_district, districts))
            
        def get_temperature_at_time(temperature_forecast, target_time):
            # Convert the target_time to a datetime object with a default time of 2 PM
            target_time = target_time.replace(hour=14, minute=0)

            # Iterate through the hourly_time list in the forecast
            for i, forecast_time_str in enumerate(temperature_forecast.hourly_time):
                # Convert the forecast_time_str to a datetime object
                forecast_time = datetime.fromisoformat(forecast_time_str)

                # Find the index where the forecast_time matches or is greater than the target_time
                if forecast_time >= target_time:
                    return temperature_forecast.hourly_temperature_2m[i]

            # If the target_time is beyond the forecast data, return None or an appropriate value
            return None

        try:
            # Get district data for source and destination
            source_forecast = TemperatureForecast.objects.filter(district__name__iexact=source_location).first()
            destination_forecast = TemperatureForecast.objects.filter(district__name__iexact=destination_location).first()

            # Convert the user date string to a datetime object with a default time of 2 PM
            target_time = datetime.strptime(travel_date, "%d-%m-%Y").replace(hour=14, minute=0)

            # Call the function to get the temperature at the target time
            source_temperature_2pm = get_temperature_at_time(source_forecast, target_time)
            destination_temperature_2pm = get_temperature_at_time(destination_forecast, target_time)

            source_location = source_location.title()
            destination_location = destination_location.title()
            recommendation_message = (
                f"Your {source_location} is {'cooler' if source_temperature_2pm < destination_temperature_2pm else 'warmer'} "
                f"than your destination {destination_location}. "
                f"{'Stay at home.' if source_temperature_2pm < destination_temperature_2pm else 'Traveling is a good idea.'}"
            )

            response_data = {
                "source_location": source_location,
                "destination_location": destination_location,
                "source_temperature_2pm": f"{source_temperature_2pm}°C",
                "destination_temperature_2pm": f"{destination_temperature_2pm}°C",
                "recommendation_message": recommendation_message
            }

            return Response(response_data)
        except District.DoesNotExist:
            return Response({"error": "District not found for the given location"}, status=400)
