import random

import factory
from phonenumbers import PhoneNumberType, example_number_for_type

from . import models


class PostalCodeFactory(factory.DjangoModelFactory):
    code = factory.LazyAttribute(lambda x: random.randrange(0000, 9999))

    class Meta:
        model = models.PostalCode


class RecipientFactory(factory.DjangoModelFactory):
    name = "Charles Darrow"
    postal_code: models.PostalCode = factory.SubFactory(PostalCodeFactory)
    phone_number = example_number_for_type(region_code="AU", num_type=PhoneNumberType.MOBILE)

    class Meta:
        model = models.Recipient
        django_get_or_create = ("name", "postal_code", "phone_number")
