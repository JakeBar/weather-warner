import logging

import requests
from requests import HTTPError
from simplejson.scanner import JSONDecodeError

API_KEY = "fece651f3db440bfaf971cabec436684"

log = logging.getLogger(__name__)


class WeatherBitException(Exception):
    pass


class WeatherBitClient(object):
    """
    WeatherBitClient - Client interface for the weatherbit API. Used to retrieve weather data
    Read more at https://www.weatherbit.io/api
    """

    def __init__(self):
        self.api_key = API_KEY
        self.base_url = "https://api.weatherbit.io/v2.0/"

    def handle_request(self, request_url: str, params) -> dict:
        """
        Perform the request to the WeatherBit API.
        Convert the response to json and handle errors along the way.
        """
        try:
            response = requests.get(request_url, params=params)
            response.raise_for_status()
            return response.json()
        except (HTTPError, JSONDecodeError) as exc:
            raise WeatherBitException(exc)
        return response.content

    def get_hourly_forecast(self, postal_code: int, hours=24, country="Australia") -> dict:
        """
        Get the hourly forecast for an area.
        https://www.weatherbit.io/api/weather-forecast-120-hour
        """
        request_url = f"{self.base_url}forecast/hourly"
        query_params = {
            "key": self.api_key,
            "hours": hours,
            "country": country,
            "postal_code": postal_code,
        }
        response = self.handle_request(request_url, query_params)
        return response["data"]