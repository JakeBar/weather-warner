import logging

from django.conf.urls import url
from django.contrib import admin, messages
from django.http import HttpResponseRedirect

from .clients.twilio import send_text
from .clients.weatherbit import WeatherBitClient
from .forecast import evaluate_data, generate_best_message
from .models import MessageChunk, PostalCode, Recipient

log = logging.getLogger(__name__)


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    change_form_template = "admin/change_form.html"
    list_filter = ("verified", "subscribed")
    list_display = ("name", "verified", "subscribed")

    def get_urls(self):
        urls = super(RecipientAdmin, self).get_urls()
        extra = [
            url(r"^(.+)/test-sms/$", self.admin_site.admin_view(self.test_sms), name="sms_testing")
        ]
        return extra + urls

    def test_sms(self, request, pk):
        try:
            recipient = Recipient.objects.get(pk=pk)
            client = WeatherBitClient()

            # Get the weather data and evaluate
            log.info("recipient.postal_code.code = %s", recipient.postal_code.code)
            hourly_forecast = client.get_hourly_forecast(postal_code=recipient.postal_code.code)
            data_points = evaluate_data(hourly_forecast)

            # Generate a message and send it
            message = generate_best_message(recipient, data_points)
            if send_text(phone_number=recipient.phone_number.as_e164, message=message):
                self.message_user(request, f"SMS successfully sent to {recipient.phone_number}.")
            else:
                raise Exception("Twilio failed for some reason")
        except Exception as ex:
            self.message_user(request, f"SMS could not be sent {str(ex)}", level=messages.ERROR)
            log.exception("SMS could not be sent")

        return HttpResponseRedirect("../change/")


admin.site.register(PostalCode)
admin.site.register(MessageChunk)
