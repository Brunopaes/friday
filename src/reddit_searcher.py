# -*- coding: utf-8 -*-
import helpers

import praw
import os


class Bot:
    def __init__(self, subreddit):
        self.subreddit = subreddit
        self.reddit = self.authenticate()

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
        """This function monitor the whitelisted subreddits seeking for new
        posts.

        Returns
        -------

        """
        for submission in self.reddit.subreddit(self.subreddit).hot(limit=10):
            print(submission.url)

    def __call__(self, *args, **kwargs):
        self.monitor()


if __name__ == '__main__':
    Bot('wtsstadamit').__call__()
