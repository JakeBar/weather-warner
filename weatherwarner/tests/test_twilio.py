from django.test import TestCase
from mock import patch
from phonenumber_field.phonenumber import PhoneNumber
from requests import HTTPError
from twilio.base.exceptions import TwilioException
from twilio.rest import Client

from weatherwarner.clients.twilio import send_text


class TwilioTestCase(TestCase):
    def setUp(self):
        self.phone_number = PhoneNumber.from_string("+15 005 550 006")
        self.message = "Hi there, the weather will be great today!"

    @patch.object(Client, "messages")
    def test_twilio_success(self, mock_method):
        mock_method.create.return_value = "Hi there, the weather will be great today!"
        response = send_text(self.phone_number.as_e164, self.message)
        self.assertTrue(response)

    @patch.object(Client, "messages")
    def test_twilio_failure(self, mock_method):
        # Twilio Specific Exception
        mock_method.create.side_effect = TwilioException
        response = send_text(self.phone_number.as_e164, self.message)
        self.assertFalse(response)

        # Generic Request Exception
        mock_method.create.side_effect = HTTPError
        response = send_text(self.phone_number.as_e164, self.message)
        self.assertFalse(response)
