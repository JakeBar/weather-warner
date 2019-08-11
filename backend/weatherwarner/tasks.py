from .clients.twilio import send_text
from .clients.weatherbit import WeatherBitClient
from .forecast import evaluate_data, generate_best_message
from .models import PostalCode


def send_weather_report():
    """
    Send a weather report via SMS to each recipient
    Returns: int
    """

    postal_codes = PostalCode.objects.prefetch_related("recipients")
    client = WeatherBitClient()

    total_sent = 0

    # For each postal code
    for postal_code in postal_codes:
        recipients = postal_code.recipients.filter(subscribed=True)
        if recipients:
            # Get the weather data and evaluate
            hourly_forecast = client.get_hourly_forecast(postal_code=postal_code.code)
            data_points = evaluate_data(hourly_forecast)

            # For each recipient in that postal code
            for recipient in postal_code.recipients.filter(subscribed=True):
                # Generate a message and send it
                message = generate_best_message(recipient, data_points)
                if send_text(phone_number=recipient.phone_number.as_e164, message=message):
                    total_sent += 1

    return total_sent
