from django.core.management.base import BaseCommand


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
        # TODO
        # send_weather_reports()
        print("Finished sending reports")
