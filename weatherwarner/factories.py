import factory
from phonenumbers import PhoneNumberType, example_number_for_type

from . import models


class PostalCodeFactory(factory.DjangoModelFactory):
    code = 3000

    class Meta:
        model = models.PostalCode


class RecipientFactory(factory.DjangoModelFactory):
    name = "Charles Darrow"
    postal_code: models.PostalCode = factory.SubFactory(PostalCodeFactory)
    phone_number = example_number_for_type(region_code="NZ", num_type=PhoneNumberType.MOBILE)

    class Meta:
        model = models.Recipient
        django_get_or_create = ("name", "postal_code")
