# -*- coding: utf-8 -*-
import datetime


class CalcETA:
    def __call__(self, *args, **kwargs):
        avengers = \
            datetime.datetime.today().replace(day=9, month=12, year=2020,
                                              hour=21, minute=00, second=0,
                                              microsecond=0)
        date = abs(datetime.datetime.today() - avengers)

        m, s = divmod(date.seconds, 60)
        h, m = divmod(m, 60)

        return '{:d} days {:d} hours {:02d} minutes {:02d} seconds'.\
            format(date.days, h, m, s)
