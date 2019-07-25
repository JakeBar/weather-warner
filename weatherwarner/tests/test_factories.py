from django.test import TestCase
from weatherwarner.factories import PostalCodeFactory, RecipientFactory
from weatherwarner.models import PostalCode, Recipient


class FactoriesTestCase(TestCase):
    def test_postal_code_factory(self):
        instance = PostalCodeFactory()
        self.assertEqual(type(instance), PostalCode)

    def test_recipient_factory(self):
        instance = RecipientFactory()
        self.assertEqual(type(instance), Recipient)
