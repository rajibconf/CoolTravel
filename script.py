"""script.py"""
# PYTHON IMPORTS
import json
import requests
# DJANGO IMPORTS
from django.http import JsonResponse
# APP IMPORTS
from coolapp.models import District


def import_district_data():
    # Specify the encoding as 'utf-8' when opening the JSON file
    with open('fixtures/bd-districts.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for district_data in data['districts']:
        District.objects.create(
            id=district_data['id'],
            division_id=district_data['division_id'],
            name=district_data['name'],
            bn_name=district_data['bn_name'],
            lat=district_data['lat'],
            long=district_data['long']
        )

# import_district_data()


def get_weather_data():
    # Define the API URL
    api_url = "https://api.open-meteo.com/v1/forecast"

    # Define the parameters for the API request
    params = {
        "latitude": 23.7104,
        "longitude": 90.4074,
        "hourly": "temperature_2m",
        "timezone": "auto"
    }

    try:
        # Make the API request
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception if the request fails

        # Parse the JSON response
        data = response.json()
        print(data)
        # You can now process the 'data' variable, which contains the API response

        return JsonResponse(data)  # Return the data as a JSON response
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": "API request failed"}, status=500)


get_weather_data()
