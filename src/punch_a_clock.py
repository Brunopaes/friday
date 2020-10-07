#!-*- coding: utf8 -*-
from selenium.webdriver.support.ui import Select
from selenium.common import exceptions
from selenium import webdriver

import helpers
import time


class NexusRPA:
    def __init__(self):
        self.driver = webdriver.Chrome(
            r'D:\PythonProjects\Personal\python-sandbox\drivers'
            r'\chromedriver.exe'
        )
        self.credentials = helpers.read_json('credentials.json')
        self.url = 'https://banco_abc.nexusweb.com.br/'
        self.alert = None

    # Used in __call__
    def opening_page(self):
        """This function opens the webdriver and access the nexus webpage.

        Returns
        -------

        """
        self.driver.get(self.url)
        self.driver.fullscreen_window()

    # Used in __call__
    def filling_form(self):
        """This function fills the website's form.

        Returns
        -------

        """
        Select(
            self.driver.find_element_by_xpath('//*[@id="cboCampo"]')
        ).select_by_index(2)

        cpf = self.driver.find_element_by_xpath('//*[@id="txtValor"]')
        cpf.clear()
        cpf.send_keys(self.credentials.get('cpf'))

        password = self.driver.find_element_by_xpath('//*[@id="txtSENHA"]')
        password.clear()
        password.send_keys(self.credentials.get('token'))

        captcha = self.driver.find_element_by_xpath(
            '//*[@id="captchacode"]')
        captcha.clear()
        captcha.send_keys(helpers.ocr(r'../data/a.png'))

        Select(
            self.driver.find_element_by_xpath('//*[@id="cboLocal"]')
        ).select_by_index(1)

        self.driver.find_element_by_xpath('//*[@id="btOk"]').click()

        self.handling_alert()

    # Used in __call__
    @staticmethod
    def buffer(seconds=2):
        """Buffer function.

        Parameters
        ----------
        seconds : int, float, optional
            Sleeping time in seconds.

        Returns
        -------

        """
        time.sleep(seconds)

    # Used in __call__
    def handling_alert(self):
        """This function handles the javascript alert.

        Returns
        -------

        """
        try:
            alert = self.driver.switch_to.alert
            self.alert = alert.text
            alert.accept()
        except exceptions.NoAlertPresentException:
            pass

    def __call__(self, *args, **kwargs):
        self.opening_page()
        while True:
            self.driver.save_screenshot(r'../data/a.png')
            helpers.crop_image('../data/a.png', (870, 600, 1050, 650))
            self.filling_form()
            self.buffer()
            self.handling_alert()

            if self.alert is not None:
                self.driver.close()
                return self.alert
