import datetime

from babel.dates import format_datetime
from loguru import logger


class LocalDate:
    def __init__(self, data: dict, lang: str, main: bool):
        self.time, self.date, self.weekday = self._localdate(data, lang, main)

    def _localdate(self, local: dict, lang, main):
        tz = datetime.timedelta(minutes=local["time_zone_offset"])
        dt = datetime.datetime.fromisoformat(local["local"])
        date = format_datetime(datetime=dt, format="HH:mm, EEEE, d MMMM", locale=lang)

        logger.debug(list(map(lambda s: s.strip(), str(date).split(','))))
        time, weekday, date = map(lambda s: s.strip().title(), str(date).split(','))
        time = (datetime.datetime.utcnow() + tz).strftime("%H:%M") if main else time
        return time, date, weekday

    def __repr__(self):
        cls = self.__class__.__name__
        return f"<{cls} {{time: {self.time}, date: {self.date}, weekday: {self.weekday}}}>"
