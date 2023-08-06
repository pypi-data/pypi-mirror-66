import logging

from flask_wtf import Form
from wtforms import StringField, TextAreaField, validators, SubmitField, ValidationError
from croniter import croniter

log = logging.getLogger(__name__)


class CronAlarmForm(Form):
    nick = StringField(
        "Alarm nick",
        validators=[validators.required()],
        description="A simple name to recognize this alarm",
    )
    cron_format = StringField(
        "cron-like format",
        validators=[validators.required()],
        description="the frequency specification, as in the <tt>cron</tt> command; "
        'see <a href="https://crontab.guru/">crontab.guru</a> for a hepl with cron format',
    )
    exclude = TextAreaField(
        "cron-like format; any matching time will be excluded",
        description="Another cron-like thing to _exclude_ events",
    )
    submit = SubmitField("Submit")

    def populate_from_timespec(self, timespec):
        if "nick" in timespec:
            self.nick.data = timespec["nick"]
        if "cron_format" in timespec:
            self.cron_format.data = timespec["cron_format"]
        if "exclude" in timespec:
            if type(timespec["exclude"]) is str:
                self.exclude.data = timespec["exclude"]
            else:
                self.exclude.data = "\n".join(timespec["exclude"])

    def validate_cron_format(self, field):
        if not croniter.is_valid(field.data):
            raise ValidationError("formato di cron non valido")

    def validate_exclude(self, field):
        for line in field.data.split("\n"):
            if line.strip() and not croniter.is_valid(line):
                raise ValidationError("formato di exclude non valido: %s" % line)


def cronalarm_receive(form):
    return {
        "kind": "cron",
        "nick": form.nick.data,
        "cron_format": form.cron_format.data,
        "exclude": [
            line.strip() for line in form.exclude.data.split("\n") if line.strip()
        ],
    }
