"""coolapp > utils.py"""
import logging
import requests
import json

logger = logging.getLogger(__name__)


def get_temperature_forecast(lat, long):
    """Get the hourly temperature forecast for a given latitude and longitude.

    Args:
        lat (float): The latitude of the location.
        long (float): The longitude of the location.

    Returns:
        list: A list of floats representing the temperature in degrees Celsius for each hour. # noqa
        None: If the API request fails or the data is invalid.
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_2m&timezone=auto&forecast_days=7" # forecast_days=(1,16) # noqa
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200 # noqa
        data = response.json()  # Parse the JSON data
        # Return a list of temperatures using a list comprehension
        return [temp for temp in data["hourly"]["temperature_2m"]]
    except requests.exceptions.RequestException as e:
        # Handle any HTTP errors
        logger.debug(f"An error occurred while requesting {url}: {e}")
    except json.decoder.JSONDecodeError as e:
        # Handle any JSON parsing errors
        logger.debug(f"An error occurred while decoding {response.text}: {e}")
    return None


def get_temperature_forecast_raw(lat, long):
    """Get the hourly temperature forecast for a given latitude and longitude.
    """

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_2m&timezone=auto&forecast_days=7" # forecast_days=(1,16) # noqa
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the status code is not 200 # noqa
        data = response.json()  # Parse the JSON data
        return data
    except requests.exceptions.RequestException as e:
        # Handle any HTTP errors
        logger.debug(f"An error occurred while requesting {url}: {e}")
    except json.decoder.JSONDecodeError as e:
        # Handle any JSON parsing errors
        logger.debug(f"An error occurred while decoding {response.text}: {e}")
    return None
