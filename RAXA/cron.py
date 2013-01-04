from django_cron import CronJobBase, Schedule
from backend.models.Timer import Timer

class Timers(CronJobBase):
    RUN_EVERY_MINS = 15

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'RAXA.cron.Timers'    # a unique code

    def do(self):
        timers = Timer.get_timers_within(self.RUN_EVERY_MINS)
        for timer in timers:
            timer.execute()