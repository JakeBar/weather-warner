from collections import Counter

from django.conf import settings

from .models import Recipient


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

    # Percentage of Precipitation
    pops = [iteration["pop"] for iteration in forecast]
    results["average_pop"] = sum(pops) / len(pops)

    # Wind Speed
    wind_speeds = [iteration["wind_spd"] for iteration in forecast]
    results["average_wind_speed"] = sum(wind_speeds) / len(wind_speeds)

    return results


def generate_best_message(recipient: Recipient, data_points: dict) -> str:
    """
    Construct a relevant message based on the data points
    returns: str
    """

    # Default Message
    message = (
        f"Morning {recipient.name}, "
        f"expect of high of {data_points['max_temp']} "
        f"and a low of {data_points['min_temp']} today."
    )

    # Forecast for windy day
    if data_points["average_wind_speed"] > settings.WIND_SPEED_THRESHOLD:
        message = (
            f"Morning {recipient.name}, " f"hold on tight, because today is going to be windy!"
        )

    # Forecast for rain
    if data_points["average_pop"] > settings.PERCENTAGE_OF_PRECIPITATION_THRESHOLD:
        message = f"Morning {recipient.name}, " f"make sure to bring a rain coat today!"

    return message
