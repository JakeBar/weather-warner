from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField


class PostalCode(models.Model):
    """
    Postal Code used for querying the weather forecast. Designed for AU postcodes.
    e.g. 3025, 2000, etc.
    """

    code = models.IntegerField(
        primary_key=True, db_index=True, validators=[MaxValueValidator(9999)]
    )

    def __str__(self):
        return f"{self.code}"


class PostCode(models.Model):
    """
    Postal Code used for querying the weather forecast. Designed for AU postcodes.
    e.g. 3025, 2000, etc.
    """

    code = models.IntegerField(validators=[MaxValueValidator(9999)])

    def __str__(self):
        return f"{self.code}"


class Recipient(models.Model):
    """
    Recipient - A user of Weather Warner
    """

    name = models.CharField(max_length=256)
    postal_code = models.ForeignKey(PostalCode, related_name="recipients", on_delete=models.CASCADE)
    postcode = models.ForeignKey(PostCode, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(unique=True, help_text="The phone number to receive the texts")
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verified = models.BooleanField(default=False)
    subscribed = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.phone_number}] {self.name} {self.postal_code}"

    def save(self, *args, **kwargs):
        self.verification_code = get_random_string(length=6, allowed_chars="0123456789ABCDEF")
        super().save(*args, **kwargs)

    @property
    def customer_friendly_number(self):
        return self.phone_number.as_e164
