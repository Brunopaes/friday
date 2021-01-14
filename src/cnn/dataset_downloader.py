# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from tqdm import tqdm

import requests
import io
import os


class ImageDownloader:
    def __init__(self):
        self.base_url = \
            'http://people.csail.mit.edu/brussell/research/LabelMe/Images/'

    @staticmethod
    def accessing_page(url):
        return requests.get(url).content

    @staticmethod
    def soup(html):
        return BeautifulSoup(html, 'html5lib')

    def downloading_images(self, soup, url):
        for image_url in tqdm(['{}/{}'.format(url, a.text) for a in
                               soup.find_all('a')[5:]]):
            filename = os.path.abspath('data/dataset/{}'.format(
                image_url.split('//')[-1])
            )
            with io.open(filename, 'wb') as file:
                file.write(self.accessing_page(image_url))

    def __call__(self, *args, **kwargs):
        soup = self.soup(self.accessing_page(self.base_url))

        for url in ['{}/{}'.format(self.base_url, a.text) for a in
                    soup.find_all('a')[18:]]:
            self.downloading_images(self.soup(self.accessing_page(url)), url)


if __name__ == '__main__':
    ImageDownloader().__call__()
