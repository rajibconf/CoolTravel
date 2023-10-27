# views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from coolapp.models import District
from API.serializers import DistrictSerializer
from concurrent.futures import ThreadPoolExecutor
from django.core.cache import cache
from coolapp.utils import get_temperature_forecast


class CoolestDistricts(APIView):
    def get(self, request):
        # Check if the data is cached
        cached_data = cache.get("coolest_districts")

        if cached_data is not None:
            return Response(cached_data)

        districts = District.objects.all()

        def fetch_and_process_district(district):
            temperature_data = get_temperature_forecast(district.lat, district.long)
            print(temperature_data, "temperature_data")
            print(temperature_data[3:10], "temperature_data[3:10]")
            average_temperature = round(sum(temperature_data[3:10]) / 7, 1) if temperature_data else None
            return {
                "id": district.id,
                "name": district.name,
                "bn_name": district.bn_name,
                "lat": district.lat,
                "long": district.long,
                "average_temperature_2pm": average_temperature
            }

        with ThreadPoolExecutor() as executor:
            # Use `map` to parallelize the execution of `fetch_and_process_district`
            coolest_districts = list(executor.map(fetch_and_process_district, districts))

        # Sort the list of districts by average temperature (coolest first)
        coolest_districts.sort(key=lambda x: x['average_temperature_2pm'])

        # Get the top 10 coolest districts
        top_10_coolest = coolest_districts[:10]

        # Cache the data for future requests (with a reasonable expiration time)
        cache.set("coolest_districts", top_10_coolest, 3600)  # Cache data for 1 hour

        return Response(top_10_coolest)
