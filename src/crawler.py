from src.lang_processing import NLTK

from selenium.webdriver.common.keys import Keys
from sklearn.naive_bayes import MultinomialNB
from selenium import webdriver
from bs4 import BeautifulSoup

import time
import os


class Message:
    def __init__(self):
        self.path = os.path.abspath(os.getcwd() + os.sep + os.pardir + '/dependencies/chromedriver')
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--user-data-dir=./User_Data')
        self.driver = webdriver.Chrome(self.path, chrome_options=self.options)
        self.url = 'https://web.whatsapp.com'

        self.driver.get('http://web.whatsapp.com')

        self.nltk = NLTK(MultinomialNB)

        self.librarian = self.nltk.cleaning_dict()
        self.model = self.nltk.fit(self.librarian)

    def get_unread(self):
        try:
            unread_chat = self.driver.find_element_by_css_selector('.OUeyt')
            unread_chat.click()

            time.sleep(3)

            self.get_last_message()

        except Exception:
            pass

    def get_source_code(self):
        html = self.driver.page_source
        return BeautifulSoup(html, 'html.parser')

    def get_last_message(self):
        soup = self.get_source_code()

        lst_msg = soup.find_all('span', {'class': 'selectable-text invisible-space copyable-text'})
        try:
            msg = lst_msg[-1].text

            if '!quit' in msg.lower():
                quit()
            elif '!pause' in msg.lower():
                if int(msg.split(' ')[-1]) > 3600:
                    input_box = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
                    input_box.send_keys('Cannot pause for more than 3600 seconds!')
                    input_box.send_keys(Keys.ENTER)
                else:
                    input_box = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
                    input_box.send_keys('Pausing for {} seconds!'.format(msg.split(' ')[-1]))
                    input_box.send_keys(Keys.ENTER)
                    time.sleep(int(msg.split(' ')[-1]))
            elif '@pause' in msg.lower():
                input_box = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
                input_box.send_keys('Overriding pause command for {} seconds!'.format(msg.split(' ')[-1]))
                input_box.send_keys(Keys.ENTER)
                time.sleep(int(msg.split(' ')[-1]))
            else:
                input_box = self.driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
                input_box.send_keys(self.nltk.pred(self.model, msg, self.librarian))
                input_box.send_keys(Keys.ENTER)

        except Exception:
            pass

    def __call__(self, *args, **kwargs):
        print('Starting API')
        input()

        while True:
            self.get_unread()


if __name__ == '__main__':
    Message().__call__()
