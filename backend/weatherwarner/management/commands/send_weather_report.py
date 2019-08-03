from django.core.management.base import BaseCommand

from weatherwarner.tasks import send_weather_report


class Command(BaseCommand):
    help = """\
Send the day's weather report to all users via test (SMS). Example usage:
./shortcuts.sh send_weather_report
"""

    def handle(self, *args, **kwargs):
        """
        Main Execution func
        """
        print("Being sending reports")
        send_weather_report()
        print("Finished sending reports")
