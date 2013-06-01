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
from RAXA.settings import TIMER_MINUTES_BETWEEN
from backend.models.Timer import Timer


class Command(BaseCommand):
    args = ''
    help = 'Run timers, should be runned by cron every %i minutes' % TIMER_MINUTES_BETWEEN

    def handle(self, *args, **options):
        timers = Timer.get_timers_within(TIMER_MINUTES_BETWEEN)
        for timer in timers:
            timer.execute()