import datetime


class NflWeekFinder(object):
    """Finds NFL Sundays"""
    SUNDAY = 6

    def __init__(self, date):
        self.date = date

    def next_sunday(self):
        days_ahead = self.SUNDAY - self.date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return self.date + datetime.timedelta(days_ahead)

    def get_nfl_sunday(self):
        if self.date.weekday() == self.SUNDAY:
            return self.date
        return self.next_sunday()
