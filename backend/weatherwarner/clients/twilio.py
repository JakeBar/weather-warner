import logging

from django.conf import settings
from phonenumber_field.phonenumber import PhoneNumber
from twilio.base.exceptions import TwilioException
from twilio.rest import Client

log = logging.getLogger(__name__)


def send_text(phone_number: PhoneNumber, message: str):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(
            body=message, from_=settings.TWILIO_FROM_NUMBER, to=phone_number
        )
    except TwilioException as e:
        log.exception("Twilio exception occurred: %s", e)
        return False
    except Exception as e:
        log.exception(e)
        return False
    else:
        log.info('SMS sent to %s. "%s"', phone_number, message)
        return True
