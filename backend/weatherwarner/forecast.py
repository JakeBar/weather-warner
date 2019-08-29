import random
from collections import Counter
from datetime import datetime

import attr
from django.conf import settings

from .models import MessageChunk, Recipient

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

DEFAULT_MESSAGE_CHUNKS = ["today is looking a-okay 👌", "kick back and relax."]
RAIN_MESSAGE_CHUNKS = ["make sure to bring an umbrella today ☂️"]
HOT_MESSAGE_CHUNKS = ["hope you live a in fridge, because today is bloody hot."]
COLD_MESSAGE_CHUNKS = ["brr did someone leave the fridge open? 🥶"]
WIND_MESSAGE_CHUNKS = ["hold on tight because today is going to be windy!"]


@attr.s(slots=True)
class Forecast(object):
    timestamp_local: str = attr.ib()
    wind_gust_spd: float = attr.ib(converter=float)
    wind_spd: float = attr.ib(converter=float)
    wind_cdir_full: str = attr.ib()
    temp: float = attr.ib(converter=float)
    app_temp: float = attr.ib(converter=float)
    pop: int = attr.ib(converter=int)
    precip: int = attr.ib(converter=int)
    snow: int = attr.ib(converter=int)
    rh: float = attr.ib(converter=float)
    clouds: int = attr.ib(converter=int)
    weather = attr.ib()


def get_most_frequent_value(values: list) -> str:
    tally = Counter(values)
    return tally.most_common(1)[0][0]


def evaluate_data(forecasts: list) -> dict:
    """
    Get key data points for the forecast.
    See https://www.weatherbit.io/api/weather-forecast-120-hour
    Returns: dict
    """
    results = {"general": {}, "rain": {}, "clouds": {}, "wind": {}}

    filtered = [{k: v for k, v in forecast.items() if k in KEYPOINTS} for forecast in forecasts]
    forecasts = [Forecast(**data) for data in filtered]

    # Highest & Lowest Temperature
    results["general"]["min_temp"] = sorted(forecasts, key=lambda x: x.temp)[0].temp
    results["general"]["max_temp"] = sorted(forecasts, key=lambda x: x.temp)[-1].temp

    # Temperature peak
    max_temp_peak = sorted(forecasts, key=lambda x: x.temp)[-1]
    results["general"]["max_temp_peak_time"] = datetime.strptime(
        max_temp_peak.timestamp_local, "%Y-%m-%dT%H:%M:%S"
    )

    # Percentage of Precipitation
    pops = [forecast.pop for forecast in forecasts]
    results["rain"]["average_pop"] = round(sum(pops) / len(pops), 1)

    max_pop_forecast = sorted(forecasts, key=lambda x: x.pop)[-1]
    results["rain"]["max_pop_peak"] = max_pop_forecast.pop
    results["rain"]["max_pop_peak_time"] = datetime.strptime(
        max_pop_forecast.timestamp_local, "%Y-%m-%dT%H:%M:%S"
    )

    max_precip_forecast = sorted(forecasts, key=lambda x: x.precip)[-1]
    results["rain"]["precip_peak"] = max_precip_forecast.precip
    results["rain"]["precip_peak_time"] = datetime.strptime(
        max_precip_forecast.timestamp_local, "%Y-%m-%dT%H:%M:%S"
    )

    # Wind Speed
    wind_speeds = [iteration.wind_spd for iteration in forecasts]
    results["wind"]["average_wind_speed"] = round(sum(wind_speeds) / len(wind_speeds), 1)
    results["wind"]["max_gust_speed"] = round(max(wind_speeds), 1)

    # Cloud coverage
    cloud_coverages = [iteration.clouds for iteration in forecasts]
    results["clouds"]["average_cloud_coverage"] = round(
        sum(cloud_coverages) / len(cloud_coverages), 1
    )
    results["clouds"]["max_cloud_coverage"] = round(max(cloud_coverages), 1)
    results["clouds"]["min_cloud_coverage"] = round(min(cloud_coverages), 1)

    # Most Frequent Description
    descriptions = [iteration.weather["description"] for iteration in forecasts]
    results["general"]["most_frequent_description"] = get_most_frequent_value(descriptions)

    return results


def generate_best_message(recipient: Recipient, data_points: dict) -> str:
    """
    Construct a relevant message based on the data points
    returns: str
    """

    # Start of message
    message = f"Morning {recipient.name}, "

    # Forecast for rain
    if data_points["rain"]["average_pop"] > settings.PERCENTAGE_OF_PRECIPITATION_THRESHOLD:
        choices = RAIN_MESSAGE_CHUNKS + list(
            MessageChunk.objects.filter(forecast_type="RAIN").values_list("message", flat=True)
        )
        message += random.choice(choices)

        precipitation = data_points["rain"]["precip_peak"]
        time = data_points["rain"]["precip_peak_time"].strftime("%-I%p")
        message += f"Up to {precipitation}mm rain at {time}. "

    # Forecast for hot day
    elif data_points["general"]["max_temp"] > settings.MAX_TEMP_THRESHOLD:
        choices = RAIN_MESSAGE_CHUNKS + list(
            MessageChunk.objects.filter(forecast_type="HOT").values_list("message", flat=True)
        )
        message += random.choice(choices)

    # Forecast for cold day
    elif data_points["general"]["min_temp"] < settings.MIN_TEMP_THRESHOLD:
        choices = COLD_MESSAGE_CHUNKS + list(
            MessageChunk.objects.filter(forecast_type="COLD").values_list("message", flat=True)
        )
        message += random.choice(choices)

    # Forecast for windy day
    elif data_points["wind"]["average_wind_speed"] > settings.WIND_SPEED_THRESHOLD:
        choices = WIND_MESSAGE_CHUNKS + list(
            MessageChunk.objects.filter(forecast_type="WIND").values_list("message", flat=True)
        )
        message += random.choice(choices)
        gust_speed = data_points["wind"]["max_gust_speed"]
        message += f"Gusts of up to {gust_speed}km/hr. "

    # Default
    else:
        default_choices = DEFAULT_MESSAGE_CHUNKS + list(
            MessageChunk.objects.filter(forecast_type="DEFAULT").values_list("message", flat=True)
        )
        message += random.choice(default_choices)

    # End of message
    message += (
        f" Expect a high of {data_points['general']['max_temp']}°C "
        f"and a low of {data_points['general']['min_temp']}°C."
    )

    return message
