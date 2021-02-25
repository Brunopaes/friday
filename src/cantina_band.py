# -*- coding: utf-8 -*-
import pornhub_api
import random


class CantinaBand:
    def __init__(self, filter):
        self.api = pornhub_api.PornhubApi()
        self.filter = (filter.split(' ')[1:] if filter != 'porn' else 'hentai')

    def searching(self):
        """This function randomly returns a pornhub video - for a given tag.

        Returns
        -------
        url : str
            Pornhub's video url.

        """
        try:
            return random.choice(
                [i.url for i in self.api.search.search(
                    ordering='mostviewed',
                    category=self.filter
                ).videos]
            ).title().lower()
        except Exception as e:
            e.args
            return random.choice(
                [i.url for i in self.api.search.search(
                    ordering='mostviewed',
                    tags=self.filter
                ).videos]
            ).title().lower()

    def __call__(self, *args, **kwargs):
        return self.searching()
