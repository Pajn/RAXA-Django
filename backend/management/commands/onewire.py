from django.core.management.base import BaseCommand
from backend.models.Thermometer import Thermometer


class Command(BaseCommand):
    args = '<code temp>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        code = args[0]
        temp = float(args[1])

        try:
            therm = Thermometer.objects.get(type='OneWire', code=code)
        except Thermometer.DoesNotExist:
            therm = Thermometer(type='OneWire', code=code)
            therm.name = 'New OneWire Sensor'

        therm.temperature = temp
        therm.save()
