from collections import Counter

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

    return results


def generate_best_message(recipient: Recipient, data_points: dict) -> str:
    """
    Construct a relevant message based on the data points
    """
    message = (
        f"Morning {recipient.name}, "
        f"expect of high of {data_points['max_temp']} "
        f"and a low of {data_points['min_temp']} today."
    )
    return message
