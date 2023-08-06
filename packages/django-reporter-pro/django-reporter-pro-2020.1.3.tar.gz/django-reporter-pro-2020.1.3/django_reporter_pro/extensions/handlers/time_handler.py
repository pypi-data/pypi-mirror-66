"""
Helper classes for parsers.
"""
from __future__ import unicode_literals

from datetime import timedelta, datetime

from dateutil.relativedelta import relativedelta


class TimeHandler(object):
    @classmethod
    def get_before(cls, minutes=0, hours=0, days=0, weeks=0, months=0, quarters=0, years=0, align=False):
        result_time = None
        now = datetime.now().replace(second=0, microsecond=0)
        if align:
            if years:
                result_time = now.replace(month=1, day=1, hour=0, minute=0) - relativedelta(years=years - 1)
            elif months:
                result_time = now.replace(day=1, hour=0, minute=0) - relativedelta(months=months - 1)
            elif quarters:
                result_time = now.replace(month=now.month - now.month % 3, day=1, hour=0, minute=0) - \
                              relativedelta(months=(quarters - 1) * 3)
            elif weeks:
                result_time = now.replace(hour=0, minute=0) - timedelta(days=now.weekday()) - \
                              relativedelta(weeks=weeks - 1)
            elif days:
                result_time = now.replace(hour=0, minute=0) - timedelta(days=days - 1)
            elif hours:
                result_time = now.replace(minute=0) - relativedelta(hours=hours - 1)
            elif minutes:
                result_time = now - relativedelta(minutes=minutes - 1)
        else:
            if years:
                result_time = now - relativedelta(years=years)
            elif months:
                result_time = now - relativedelta(months=months)
            elif quarters:
                result_time = now.replace(month=now.month - now.month % 3) - \
                              relativedelta(months=(quarters - 1) * 3)
            elif weeks:
                result_time = now - relativedelta(weeks=weeks)
            elif days:
                result_time = now - timedelta(days=days)
            elif hours:
                result_time = now - relativedelta(hours=hours)
            elif minutes:
                result_time = now - relativedelta(minutes=minutes)
        return result_time
