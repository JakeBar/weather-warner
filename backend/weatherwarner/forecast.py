import functools
from collections import Counter

from django.conf import settings

from .models import Recipient

KEYPOINTS = {
    "timestamp_local",
    "wind_gust_spd",
    "wind_spd",
    "wind_cdir_full",
    "temp",
    "app_temp",
    "pop",
    "precip",
    "snow",
    "rh",
    "clouds",
    "weather",
}


def get_most_frequent_value(values: list) -> str:
    tally = Counter(values)
    return tally.most_common(1)[0][0]


def evaluate_data(forecasts: list) -> dict:
    """
    Get key data points for the forecast.
    See https://www.weatherbit.io/api/weather-forecast-120-hour
    Returns: dict
    """
    results = {"general": {}, "rain": {}, "clouds": {}, "sun": {}, "wind": {}}

    filtered_forecasts = [
        {k: v for k, v in forecast.items() if k in KEYPOINTS} for forecast in forecasts
    ]

    # Highest & Lowest Temperature
    temperatures = [iteration["temp"] for iteration in filtered_forecasts]
    results["general"]["max_temp"] = round(max(temperatures), 1)
    results["general"]["min_temp"] = round(min(temperatures), 1)

    # Temperature peak
    max_temp_forecast = functools.reduce(
        lambda a, b: a if a["temp"] >= b["temp"] else b, filtered_forecasts
    )
    results["general"]["max_temp_peak"] = max_temp_forecast["temp"]
    results["general"]["max_temp_peak_time"] = max_temp_forecast["timestamp_local"]

    # Percentage of Precipitation
    pops = [iteration["pop"] for iteration in filtered_forecasts]
    results["rain"]["average_pop"] = round(sum(pops) / len(pops), 1)

    max_pop_forecast = functools.reduce(
        lambda a, b: a if a["pop"] >= b["pop"] else b, filtered_forecasts
    )
    results["rain"]["max_pop_peak"] = max_pop_forecast["pop"]
    results["rain"]["max_pop_peak_time"] = max_pop_forecast["timestamp_local"]

    max_precip_forecast = functools.reduce(
        lambda a, b: a if a["precip"] >= b["precip"] else b, filtered_forecasts
    )
    results["rain"]["max_precip_peak"] = max_precip_forecast["precip"]
    results["rain"]["max_precip_peak_time"] = max_precip_forecast["timestamp_local"]

    # Wind Speed
    wind_speeds = [iteration["wind_spd"] for iteration in filtered_forecasts]
    results["wind"]["average_wind_speed"] = round(sum(wind_speeds) / len(wind_speeds), 1)
    results["wind"]["max_gust_speed"] = round(max(wind_speeds), 1)

    # Cloud coverage
    cloud_coverages = [iteration["clouds"] for iteration in filtered_forecasts]
    results["clouds"]["average_cloud_coverage"] = round(
        sum(cloud_coverages) / len(cloud_coverages), 1
    )
    results["clouds"]["max_cloud_coverage"] = round(max(cloud_coverages), 1)
    results["clouds"]["min_cloud_coverage"] = round(min(cloud_coverages), 1)

    # Most Frequent Description
    descriptions = [iteration["weather"]["description"] for iteration in filtered_forecasts]
    results["general"]["most_frequent_description"] = get_most_frequent_value(descriptions)

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
