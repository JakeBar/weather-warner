import phonenumbers
from django.test import TestCase
from mock import patch

from weatherwarner.factories import PostCodeFactory, RecipientFactory
from weatherwarner.models import Recipient


class RequestVerificationTestCase(TestCase):
    def setUp(self):
        self.postcode = PostCodeFactory()
        self.recipient_data = {
            "name": "Jack",
            "postcode": str(self.postcode.code),
            "phone_number": "+61421955955",
        }

    @patch("weatherwarner.api.send_text")
    def test_request_verification_success(self, mock_text):
        mock_text.return_value = True

        self.assertEqual(Recipient.objects.count(), 0)

        response = self.client.post("/api/verification/request/", data=self.recipient_data)

        self.assertEqual(response.status_code, 200)

        recipient = Recipient.objects.first()

        self.assertEqual(recipient.name, self.recipient_data["name"])
        self.assertEqual(str(recipient.postcode.code), self.recipient_data["postcode"])
        self.assertEqual(recipient.customer_friendly_number, self.recipient_data["phone_number"])

        self.assertFalse(recipient.verified)
        self.assertFalse(recipient.subscribed)
        mock_text.assert_called_once()

    @patch("weatherwarner.api.send_text")
    def test_request_verification_customer_friendly(self, mock_text):
        mock_text.return_value = True
        self.recipient_data["phone_number"] = "04 21 666 222"

        self.assertEqual(Recipient.objects.count(), 0)

        response = self.client.post("/api/verification/request/", data=self.recipient_data)

        self.assertEqual(response.status_code, 200)

        recipient = Recipient.objects.first()

        self.assertEqual(recipient.name, self.recipient_data["name"])
        self.assertEqual(str(recipient.postcode.code), self.recipient_data["postcode"])

        phone_number = phonenumbers.parse(self.recipient_data["phone_number"], "AU")
        formatted_number = phonenumbers.format_number(
            phone_number, phonenumbers.PhoneNumberFormat.E164
        )
        self.assertEqual(recipient.customer_friendly_number, formatted_number)

        mock_text.assert_called_once()

    @patch("weatherwarner.api.send_text")
    def test_request_verification_customer_friendly_too_many_digits(self, mock_text):
        mock_text.return_value = True
        self.recipient_data["phone_number"] = "04 21 666 222 999999999"

        self.assertEqual(Recipient.objects.count(), 0)

        response = self.client.post("/api/verification/request/", data=self.recipient_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"phone_number": ["Invalid Phone Number. Please try another. e.g. 0421 900 800"]},
        )

        self.assertEqual(Recipient.objects.count(), 0)

    @patch("weatherwarner.api.send_text")
    def test_request_verification_invalid_number_symbols(self, mock_text):
        mock_text.return_value = True

        self.recipient_data["phone_number"] = "ABC123"

        self.assertEqual(Recipient.objects.count(), 0)

        response = self.client.post("/api/verification/request/", data=self.recipient_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"phone_number": ["The phone number entered is not valid."]}
        )

        self.assertEqual(Recipient.objects.count(), 0)

    @patch("weatherwarner.api.send_text")
    def test_request_verification_postcode_does_not_exist(self, mock_text):
        mock_text.return_value = True

        self.recipient_data["postcode"] = "9999"

        self.assertEqual(Recipient.objects.count(), 0)

        response = self.client.post("/api/verification/request/", data=self.recipient_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"postcode": ['Invalid pk "9999" - object does not exist.']}
        )

        self.assertEqual(Recipient.objects.count(), 0)

    @patch("weatherwarner.api.send_text")
    def test_request_verification_postcode_no_name(self, mock_text):
        mock_text.return_value = True

        self.recipient_data["name"] = ""

        self.assertEqual(Recipient.objects.count(), 0)

        response = self.client.post("/api/verification/request/", data=self.recipient_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"name": ["This field may not be blank."]})

        self.assertEqual(Recipient.objects.count(), 0)


class ValidateVerificationTestCase(TestCase):
    def setUp(self):
        self.postcode = PostCodeFactory()
        self.recipient = RecipientFactory(
            verification_code="123456", phone_number=phonenumbers.parse("+61421955955", "AU")
        )
        self.recipient_data = {"verification_code": self.recipient.verification_code}

    @patch("weatherwarner.api.send_text")
    def test_validation_success(self, mock_text):
        mock_text.return_value = True
        session = self.client.session
        session["phone_number"] = self.recipient.phone_number.as_e164
        session.save()

        self.assertFalse(self.recipient.verified)
        self.assertFalse(self.recipient.subscribed)

        response = self.client.post("/api/verification/validate/", data=self.recipient_data)

        self.assertEqual(response.status_code, 200)

        self.recipient.refresh_from_db()
        self.assertTrue(self.recipient.verified)
        self.assertTrue(self.recipient.subscribed)
        mock_text.assert_called_once()

    def test_validation_invalid_code(self):
        self.recipient_data["verification_code"] = "222222"
        session = self.client.session
        session["phone_number"] = self.recipient.phone_number.as_e164
        session.save()

        self.assertFalse(self.recipient.verified)
        self.assertFalse(self.recipient.subscribed)

        response = self.client.post("/api/verification/validate/", data=self.recipient_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"verification_code": ["Invalid verification code. Please try again."]}
        )

        self.recipient.refresh_from_db()
        self.assertFalse(self.recipient.verified)
        self.assertFalse(self.recipient.subscribed)

    def test_validation_invalid_code_malformed(self):
        self.recipient_data["verification_code"] = "123ZZZ"
        session = self.client.session
        session["phone_number"] = self.recipient.phone_number.as_e164
        session.save()

        self.assertFalse(self.recipient.verified)
        self.assertFalse(self.recipient.subscribed)

        response = self.client.post("/api/verification/validate/", data=self.recipient_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"verification_code": ["Invalid verification code. Please try again."]}
        )

        self.recipient.refresh_from_db()
        self.assertFalse(self.recipient.verified)
        self.assertFalse(self.recipient.subscribed)

    def test_validation_invalid_code_too_long(self):
        self.recipient_data["verification_code"] = "123ZZZZ"

        session = self.client.session
        session["phone_number"] = self.recipient.phone_number.as_e164
        session.save()

        self.assertFalse(self.recipient.verified)
        self.assertFalse(self.recipient.subscribed)

        response = self.client.post("/api/verification/validate/", data=self.recipient_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"verification_code": ["Ensure this field has no more than 6 characters."]},
        )

        self.recipient.refresh_from_db()
        self.assertFalse(self.recipient.subscribed)

    def test_validation_phone_number_does_not_exist(self):
        session = self.client.session
        session["phone_number"] = "+61421000000"
        session.save()

        self.assertFalse(self.recipient.subscribed)

        response = self.client.post("/api/verification/validate/", data=self.recipient_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"verification_code": ["Invalid verification code. Please try again."]}
        )

        self.recipient.refresh_from_db()
        self.assertFalse(self.recipient.subscribed)


class UnsubscribeTestCase(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.recipient = RecipientFactory(
            verification_code="123456", phone_number=phonenumbers.parse("+61421955955", "AU")
        )

    def test_unsubscribe_success(self):
        mock_values = {"Body": "+61421955955"}

        response = self.client.post("/api/subscription/unsubscribe/", data=mock_values)

        self.assertEqual(
            response.content,
            b'<?xml version="1.0" encoding="UTF-8"?><Response><Message>Unsubscribed! Sorry to see you go</Message></Response>',  # noqa
        )

    def test_unsubscribe_does_not_exist(self):
        mock_values = {"Body": "+61421950000"}

        response = self.client.post("/api/subscription/unsubscribe/", data=mock_values)

        self.assertEqual(response.status_code, 404)
