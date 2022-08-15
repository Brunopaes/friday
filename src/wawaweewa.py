# -*- coding: utf-8 -*-
import helpers


class Summonizer:
    def __init__(self):
        self.client = helpers.start_connection()
