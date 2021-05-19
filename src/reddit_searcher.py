# -*- coding: utf-8 -*-
import helpers

import requests
import random
import praw
import PIL
import io


class Reddit:
    def __init__(self, arguments):
        self.subreddit = arguments
        self.reddit = self.authenticate()
        self.posts = []

        self.image = None

    # used in __init__
    @staticmethod
    def authenticate():
        """This function logs in some reddit´s account.
        Returns
        -------
        """
        return praw.Reddit(
            **helpers.read_json('settings/reddit_settings.json')
        )

    # used in __call__
    def monitor(self):
        """This function extracts some random media posts from a given r/.

        Returns
        -------

        """
        try:
            for submission in self.reddit.subreddit(self.subreddit).hot():
                if submission.is_self is False:
                    self.posts.append(submission.url)
        except Exception as e:
            e.args

    # used in __call__
    def requesting(self):
        """This function requests into a given media url.

        Returns
        -------
        response : generator
            Generator package containing media bytes and filename.

        """
        tries = 0
        while tries < 10:
            try:
                chosen_one = random.choice(self.posts)
            except IndexError:
                break

            if any([i in chosen_one for i in ['jpg', 'png']]):
                return requests.get(chosen_one).content

            tries += 1
        return 'Impossible, perhaps the archives are incomplete!'

    def parsing_image(self, response):
        """This function parses image responses (jpeg and png).

        Parameters
        ----------
        response : generator
            Generator package containing media bytes.
        Returns
        -------

        """
        self.image = response if isinstance(response[0], str) \
            else PIL.Image.open(io.BytesIO(response))

    def __call__(self, *args, **kwargs):
        self.monitor()
        self.parsing_image(self.requesting())

        return self.image


if __name__ == '__main__':
    helpers.courier(Reddit('playboy').__call__(), 144068478)
