from django.test import TestCase

from weatherwarner.factories import PostCodeFactory, RecipientFactory
from weatherwarner.models import PostCode, Recipient


class FactoriesTestCase(TestCase):
    def test_postcode_factory(self):
        instance = PostCodeFactory()
        self.assertEqual(type(instance), PostCode)

    def test_recipient_factory(self):
        instance = RecipientFactory()
        self.assertEqual(type(instance), Recipient)
