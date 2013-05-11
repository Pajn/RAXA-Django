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