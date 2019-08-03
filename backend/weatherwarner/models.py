from django.core.validators import MaxValueValidator
from django.db import models
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
        return f"[{self.code}] Postal Code"


class Recipient(models.Model):
    """
    Recipient - A user of Weather Warner
    """

    name = models.CharField(max_length=256)
    postal_code = models.ForeignKey(PostalCode, related_name="recipients", on_delete=models.CASCADE)
    phone_number = PhoneNumberField(help_text="The phone number to receive the texts")

    def __str__(self):
        return f"[{self.phone_number}] {self.name} ({self.postal_code})"
