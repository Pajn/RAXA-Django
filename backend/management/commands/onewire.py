'''
Copyright (C) 2013 Rasmus Eneman <rasmus@eneman.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
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

        therm.set_temp(temp)
