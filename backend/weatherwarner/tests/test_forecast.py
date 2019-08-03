from django.test import TestCase

from weatherwarner.factories import RecipientFactory
from weatherwarner.forecast import evaluate_data, generate_best_message

SAMPLE_WEATHERBIT_DATA = [
    {
        "wind_cdir": "SSE",
        "rh": 69,
        "pod": "n",
        "timestamp_utc": "2019-07-30T11:00:00",
        "pres": 1022.58,
        "solar_rad": 0,
        "ozone": 315.223,
        "weather": {"icon": "c04n", "code": 804, "description": "Overcast clouds"},
        "wind_gust_spd": 6.50024,
        "timestamp_local": "2019-07-30T21:00:00",
        "snow_depth": 0,
        "clouds": 82,
        "ts": 1564484400,
        "wind_spd": 3.03434,
        "pop": 0,
        "wind_cdir_full": "south-southeast",
        "slp": 1030.46,
        "dni": 0,
        "dewpt": 3.2,
        "snow": 0,
        "uv": 0,
        "wind_dir": 167,
        "clouds_hi": 0,
        "precip": 0,
        "vis": 24.1348,
        "dhi": 0,
        "app_temp": 8.5,
        "datetime": "2019-07-30:11",
        "temp": 8.5,
        "ghi": 0,
        "clouds_mid": 0,
        "clouds_low": 82,
    },
    {
        "wind_cdir": "SSE",
        "rh": 72,
        "pod": "n",
        "timestamp_utc": "2019-07-30T12:00:00",
        "pres": 1022.75,
        "solar_rad": 0,
        "ozone": 317.712,
        "weather": {"icon": "c04n", "code": 804, "description": "Overcast clouds"},
        "wind_gust_spd": 6.00129,
        "timestamp_local": "2019-07-30T22:00:00",
        "snow_depth": 0,
        "clouds": 72,
        "ts": 1564488000,
        "wind_spd": 2.37176,
        "pop": 0,
        "wind_cdir_full": "south-southeast",
        "slp": 1030.69,
        "dni": 0,
        "dewpt": 3.3,
        "snow": 0,
        "uv": 0,
        "wind_dir": 165,
        "clouds_hi": 0,
        "precip": 0,
        "vis": 24.1348,
        "dhi": 0,
        "app_temp": 8.2,
        "datetime": "2019-07-30:12",
        "temp": 8.2,
        "ghi": 0,
        "clouds_mid": 0,
        "clouds_low": 72,
    },
]


class ForecastTestCase(TestCase):
    def test_evaluate_data(self):
        """
        Assert the weatherbit data is evaluated into something meaningful
        """
        self.maxDiff = None
        data_points = evaluate_data(SAMPLE_WEATHERBIT_DATA)
        expected_data = {
            "max_temp": 8.5,
            "min_temp": 8.2,
            "most_frequent_description": "Overcast clouds",
        }
        self.assertEquals(data_points, expected_data)


class MessageGeneratorTestCase(TestCase):
    def setUp(self):
        self.recipient = RecipientFactory()
        self.data_points = evaluate_data(SAMPLE_WEATHERBIT_DATA)

    def test_generate_message(self):
        """
        Assert a message is generated correctly
        """
        self.maxDiff = None
        message = generate_best_message(recipient=self.recipient, data_points=self.data_points)
        expected_message = "Morning Charles Darrow, expect of high of 8.5 and a low of 8.2 today."
        self.assertEquals(message, expected_message)
