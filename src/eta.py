# -*- coding: utf-8 -*-
import datetime


class CalcETA:
    def __call__(self, *args, **kwargs):
        eta = \
            datetime.datetime.today().replace(day=6, month=2, year=2021,
                                              hour=10, minute=30, second=0,
                                              microsecond=0)
        date = abs(datetime.datetime.today() - eta)

        m, s = divmod(date.seconds, 60)
        h, m = divmod(m, 60)

        return '{:d} days {:d} hours {:02d} minutes {:02d} seconds'.\
            format(date.days, h, m, s)
