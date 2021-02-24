# -*- coding: utf-8 -*-
import pornhub_api
import random


class CantinaBand:
    def __init__(self, tag):
        self.api = pornhub_api.PornhubApi()
        self.tag = tag.split(' ')[1:]

    def searching(self):
        """This function randomly returns a pornhub video - for a given tag.

        Returns
        -------
        url : str
            Pornhub's video url.

        """
        return random.choice(
            [i.url for i in self.api.search.search(
                ordering='rating',
                tags=self.tag
            ).videos]
        ).title().lower()

    def __call__(self, *args, **kwargs):
        return self.searching()
