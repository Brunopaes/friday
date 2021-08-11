# -*- coding: utf-8 -*-
from speedtest import Speedtest


class InternetSpeedRate:
    def __init__(self):
        self.speedtest = Speedtest()

    def get_internet_info(self):
        """ Internet rate information.

        Parameters
        ----------

        Returns
        -------

        """
        try:
            self.speedtest.download()
            self.speedtest.upload()
            return self.speedtest.results.dict()
        except Exception as e:
            e.args

    def get_download_rate(self):
        """ Internet download information.

        Parameters
        ----------

        Returns
        -------

        """
        return self.speedtest.download()

    def get_upload_rate(self):
        """ Internet upload information.

        Parameters
        ----------

        Returns
        -------

        """
        return self.speedtest.upload()


print(InternetSpeedRate().get_internet_info())
