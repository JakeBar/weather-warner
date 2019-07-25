from django.test import TestCase
from mock import patch
from requests import HTTPError
from weatherwarner.client import WeatherBitClient


class ClientTestCase(TestCase):
    def setUp(self):
        self.client = WeatherBitClient()

    @patch("requests.get")
    def test_forecast_success(self, mock_request):
        expected_data = {
            "data": [
                {
                    "wind_cdir": "WSW",
                    "rh": 68,
                    "pod": "n",
                    "timestamp_utc": "2019-07-23T12:00:00",
                    "pres": 1006.41,
                    "solar_rad": 0,
                    "ozone": 391.995,
                    "weather": {"icon": "c04n", "code": 804, "description": "Overcast clouds"},
                    "wind_gust_spd": 11.0205,
                    "timestamp_local": "2019-07-23T22:00:00",
                    "snow_depth": 0,
                    "clouds": 94,
                    "ts": 1563883200,
                    "wind_spd": 5.42351,
                    "pop": 15,
                    "wind_cdir_full": "west-southwest",
                    "slp": 1013.4,
                    "dni": 0,
                    "dewpt": 4.3,
                    "snow": 0,
                    "uv": 0,
                    "wind_dir": 244,
                    "clouds_hi": 61,
                    "precip": 0.0625,
                    "vis": 24.135,
                    "dhi": 0,
                    "app_temp": 10,
                    "datetime": "2019-07-23:12",
                    "temp": 10,
                    "ghi": 0,
                    "clouds_mid": 67,
                    "clouds_low": 79,
                }
            ],
            "city_name": "FOOTSCRAY",
            "lon": "144.9333",
            "timezone": "Australia/Melbourne",
            "lat": "-37.7833",
            "country_code": "AU",
            "state_code": "VIC",
        }
        mock_request.return_value.json.return_value = expected_data
        response = self.client.get_hourly_forecast(postal_code=3000)
        self.assertEquals(response, expected_data["data"])

    @patch("requests.get")
    def test_forecast_failure(self, mock_request):
        mock_request.side_effect = HTTPError
        with self.assertRaises(HTTPError):
            self.client.get_hourly_forecast(postal_code=3000)
