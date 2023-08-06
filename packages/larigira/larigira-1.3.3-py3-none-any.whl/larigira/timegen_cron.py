import logging
from datetime import datetime, timedelta

from croniter import croniter

from .timegen_every import Alarm

log = logging.getLogger("time-cron")


class CronAlarm(Alarm):

    description = "Frequency specified by cron-like format. nerds preferred"

    def __init__(self, obj):
        super().__init__()

        self.cron_format = obj["cron_format"]
        if "exclude" in obj:
            if type(obj["exclude"]) is str:
                self.exclude = [
                    line.strip() for line in obj["exclude"].split("\n") if line.strip()
                ]
            else:
                self.exclude = [excl for excl in obj["exclude"] if excl.strip()]
        else:
            self.exclude = []
        if not croniter.is_valid(self.cron_format):
            raise ValueError("Invalid cron_format: `%s`" % self.cron_format)
        for exclude in self.exclude:
            if not croniter.is_valid(exclude):
                raise ValueError("Invalid exclude: `%s`" % exclude)

    def is_excluded(self, dt):
        base = dt - timedelta(seconds=1)
        for exclude in self.exclude:
            nt = croniter(exclude, base).get_next(datetime)
            if nt == dt:
                return True
        return False

    def next_ring(self, current_time=None):
        if current_time is None:
            current_time = datetime.now()

        # cron granularity is to the minute
        # thus, doing 2000 attemps guarantees at least 32hours.
        # if your event is no more frequent than 10minutes, this is 13days
        for _ in range(2000):
            nt = croniter(self.cron_format, current_time).get_next(datetime)
            if not self.is_excluded(nt):
                return nt
            current_time = nt
        return None

    def has_ring(self, current_time=None):
        # cron specification has no possibility of being over
        return self.next_ring(current_time) is not None
