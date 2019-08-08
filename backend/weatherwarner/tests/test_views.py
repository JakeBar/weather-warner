import phonenumbers
from django.test import TestCase
from mock import patch

from weatherwarner.factories import PostalCodeFactory, RecipientFactory
from weatherwarner.models import Recipient


class RequestVerificationTestCase(TestCase):
    def setUp(self):
        self.postal_code = PostalCodeFactory()
        # TODO why is this so difficult?
        self.recipient_data = {
            "name": "Jack",
            "postal_code": str(self.postal_code.code),
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
        self.assertEqual(str(recipient.postal_code.code), self.recipient_data["postal_code"])
        self.assertEqual(recipient.customer_friendly_number, self.recipient_data["phone_number"])

        self.assertFalse(recipient.verified)
        mock_text.assert_called_once()

    # # TODO come back to this
    # @patch("weatherwarner.api.send_text")
    # def test_request_verification_customer_friendly(self, mock_text):
    #     mock_text.return_value = True
    #     self.recipient_data["phone_number"] = "04 219 666 222"

    #     self.assertEqual(Recipient.objects.count(), 0)

    #     response = self.client.post("/api/verification/request/", data=self.recipient_data)

    #     self.assertEqual(response.status_code, 200)

    #     recipient = Recipient.objects.first()

    #     self.assertEqual(recipient.name, self.recipient_data["name"])
    #     self.assertEqual(str(recipient.postal_code.code), self.recipient_data["postal_code"])
    #     self.assertEqual(recipient.customer_friendly_number, self.recipient_data["phone_number"])
    #     mock_text.assert_called_once()

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

        self.recipient_data["postal_code"] = "9999"

        self.assertEqual(Recipient.objects.count(), 0)

        response = self.client.post("/api/verification/request/", data=self.recipient_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"postal_code": ['Invalid pk "9999" - object does not exist.']}
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
        self.postal_code = PostalCodeFactory()
        self.recipient = RecipientFactory(
            verification_code="123456", phone_number=phonenumbers.parse("+61421955955", "AU")
        )
        self.recipient_data = {"verification_code": self.recipient.verification_code}

    def test_validation_success(self):
        session = self.client.session
        session["phone_number"] = self.recipient.phone_number.as_e164
        session.save()

        self.assertFalse(self.recipient.verified)

        response = self.client.post("/api/verification/validate/", data=self.recipient_data)

        self.assertEqual(response.status_code, 200)

        self.recipient.refresh_from_db()
        self.assertTrue(self.recipient.verified)

    def test_validation_invalid_code(self):
        self.recipient_data["verification_code"] = "222222"
        session = self.client.session
        session["phone_number"] = self.recipient.phone_number.as_e164
        session.save()

        self.assertFalse(self.recipient.verified)

        response = self.client.post("/api/verification/validate/", data=self.recipient_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"message": ["Invalid verification code. Please try again."]}
        )

        self.recipient.refresh_from_db()
        self.assertFalse(self.recipient.verified)

    def test_validation_invalid_code_malformed(self):
        self.recipient_data["verification_code"] = "123ZZZ"
        session = self.client.session
        session["phone_number"] = self.recipient.phone_number.as_e164
        session.save()

        self.assertFalse(self.recipient.verified)

        response = self.client.post("/api/verification/validate/", data=self.recipient_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"message": ["Invalid verification code. Please try again."]}
        )

        self.recipient.refresh_from_db()
        self.assertFalse(self.recipient.verified)

    def test_validation_invalid_code_too_long(self):
        self.recipient_data["verification_code"] = "123ZZZZ"

        session = self.client.session
        session["phone_number"] = self.recipient.phone_number.as_e164
        session.save()

        self.assertFalse(self.recipient.verified)

        response = self.client.post("/api/verification/validate/", data=self.recipient_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"verification_code": ["Ensure this field has no more than 6 characters."]},
        )

        self.recipient.refresh_from_db()
        self.assertFalse(self.recipient.verified)

    def test_validation_phone_number_does_not_exist(self):
        session = self.client.session
        session["phone_number"] = "+61421000000"
        session.save()

        self.assertFalse(self.recipient.verified)

        response = self.client.post("/api/verification/validate/", data=self.recipient_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"message": ["Invalid verification code. Please try again."]}
        )

        self.recipient.refresh_from_db()
        self.assertFalse(self.recipient.verified)
