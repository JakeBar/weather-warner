from collections import Counter

from .client import WeatherBitClient
from .models import PostalCode, Recipient


class MalformedDataException(Exception):
    pass


def get_most_frequent_value(values: list) -> str:
    tally = Counter(values)
    return tally.most_common(1)[0][0]


def evaluate_data(forecast: list) -> dict:
    """
    Get key data points for the forecast
    Returns: dict
    """
    results = {}

    # Most Frequent Description
    descriptions = [iteration["weather"]["description"] for iteration in forecast]
    results["most_frequent_description"] = get_most_frequent_value(descriptions)

    # Highest & Lowest Temperature
    temperatures = [iteration["temp"] for iteration in forecast]
    results["max_temp"] = max(temperatures)
    results["min_temp"] = min(temperatures)

    return results


def generate_best_message(recipient: Recipient, data_points: dict) -> str:
    """
    Construct a relevant message based on the data points
    """
    # default
    message = (
        f"Morning {recipient.name}, "
        f"expect of high of {data_points['max_temp']} "
        f"and a low of {data_points['min_temp']} today."
    )
    return message


def send_weather_report():
    """
    For each postcode tally of the subscribed users
    Get the hourly forecast
    And evaluate for value
    Returns: None
    """

    postal_codes = PostalCode.objects.all().prefetch_related("recipients")
    client = WeatherBitClient()

    total_sent = 0
    for postal_code in postal_codes:
        hourly_forecast = client.get_hourly_forecast(postal_code=postal_code.code)
        data_points = evaluate_data(hourly_forecast)
        for recipient in postal_code.recipients.all():
            text_message = generate_best_message(recipient, data_points)
            # TODO send message via Twilio
            print(text_message)
            total_sent += 1
    return total_sent
