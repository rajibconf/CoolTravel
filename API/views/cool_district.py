# views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from coolapp.models import District
from API.serializers import DistrictSerializer
from concurrent.futures import ThreadPoolExecutor
from coolapp.utils import get_temperature_forecast

class CoolestDistricts(APIView):
    def get(self, request):
        # No need to check if the data is cached, as Redis handles caching
        districts = District.objects.all()

        def fetch_and_process_district(district):
            temperature_data = get_temperature_forecast(district.lat, district.long)
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
            coolest_districts = list(executor.map(fetch_and_process_district, districts))

        # Sort the list of districts by average temperature (coolest first)
        coolest_districts.sort(key=lambda x: x['average_temperature_2pm'])

        # Get the top 10 coolest districts
        top_10_coolest = coolest_districts[:10]

        return Response(top_10_coolest)
