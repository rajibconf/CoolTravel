"""coolapp > utils.py"""
import requests

def get_temperature_forecast(lat, long):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_2m&timezone=auto"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['hourly']['temperature_2m']
    return None
