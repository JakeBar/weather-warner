import phonenumbers
from django.conf import settings
from django.db import connection, reset_queries
from django.test import TestCase
from mock import MagicMock, patch
from twilio.base.exceptions import TwilioException
from twilio.rest import Client as TwilioClient

from weatherwarner.factories import PostalCodeFactory, RecipientFactory
from weatherwarner.models import Recipient
from weatherwarner.tasks import send_weather_report

EXPECTED_WEATHERBIT_DATA = [
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
]


@patch(
    "weatherwarner.clients.weatherbit.WeatherBitClient.get_hourly_forecast",
    MagicMock(return_value=EXPECTED_WEATHERBIT_DATA),
)
class TaskRunnerTestCase(TestCase):
    def setUp(self):
        self.recipient = RecipientFactory(subscribed=True)
        self.postal_code = PostalCodeFactory()

    @patch.object(TwilioClient, "messages")
    def test_weather_report_success(self, mock_twilio):
        """
        Assert that an SMS is successfully sent to one recipient
        """
        mock_twilio.create.return_value = "Hi there, the weather will be great today!"
        result = send_weather_report()
        self.assertEquals(result, 1)

    @patch.object(TwilioClient, "messages")
    def test_weather_report_success_multiple_recipients(self, mock_twilio):
        """
        Assert multiples SMSes are successfully sent if there are two ore more recipients
        """
        self.second_recipient = RecipientFactory(
            phone_number=phonenumbers.parse("+61421951234", "AU"), subscribed=True
        )
        mock_twilio.create.return_value = "Hi there, the weather will be great today!"
        result = send_weather_report()
        self.assertEquals(result, 2)

    @patch.object(TwilioClient, "messages")
    def test_weather_report_success_unsubscribed_recipients(self, mock_twilio):
        """
        Assert multiples SMSes are successfully sent if there are two ore more recipients
        """
        self.second_recipient = RecipientFactory(subscribed=True)
        mock_twilio.create.return_value = "Hi there, the weather will be great today!"
        result = send_weather_report()
        self.assertEquals(result, 1)

    @patch.object(TwilioClient, "messages")
    def test_weather_report_success_no_recipients(self, mock_twilio):
        """
        Assert no SMSes are sent if there are no recipients
        """
        Recipient.objects.all().delete()
        mock_twilio.create.return_value = "Hi there, the weather will be great today!"
        result = send_weather_report()
        self.assertEquals(result, 0)

    @patch.object(TwilioClient, "messages")
    def test_weather_report_success_errors_handled_gracefully(self, mock_twilio):
        """
        Assert an error with the twilio client is handled gracefully
        """

        # Twilio Specific Exception
        mock_twilio.create.side_effect = TwilioException
        result = send_weather_report()
        self.assertEquals(result, 0)

        mock_twilio.create.side_effect = None
        mock_twilio.create.return_value = "Hi there, the weather will be great today!"
        result = send_weather_report()
        self.assertEquals(result, 1)

    @patch.object(TwilioClient, "messages")
    def test_minimum_number_connections_weather_report(self, mock_twilio):
        """
        Assert the number of minimum no. db connections are made for an Weather report.
        """
        for i in range(5):
            postal_code = PostalCodeFactory()
            for j in range(10):
                phone_number = f"+614219555{i}{j}"
                RecipientFactory(
                    postal_code=postal_code, phone_number=phonenumbers.parse(phone_number, "AU")
                )

        settings.DEBUG = True
        reset_queries()
        self.assertEqual(len(connection.queries), 0)

        mock_twilio.create.side_effect = None
        mock_twilio.create.return_value = "Hi there, the weather will be great today!"
        send_weather_report()

        self.assertEqual(len(connection.queries), 9)
        settings.DEBUG = False
