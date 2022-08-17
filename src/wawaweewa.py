# -*- coding: utf-8 -*-
import helpers
import random


class SummonizerList:
    def __init__(self):
        self.client = helpers.start_connection()

        self.query = ("""
            SELECT
                model_name,
                album_name,
                release_year
            FROM
                `mooncake-304003.wawaweewa.albums` AS A
            LEFT JOIN
                `wawaweewa.playmates` AS B
            ON
                A.model_name = B.full_name
            ORDER BY
                model_name
            """)

        self.results = self.querying()

    def querying(self):
        return self.client.query(self.query)

    def __call__(self, *args, **kwargs):
        return '\n'.join([' - '.join(i[0:2]) for i in self.results])


class Summonizer:
    def __init__(self, model_name, query_type='model'):
        self.model_name = ' '.join(
            [i.capitalize() for i in model_name.split(' ')]
        ) if query_type == 'model' else model_name

        self.client = helpers.start_connection()
        self.query = self.defining_query(query_type)
        self.results = self.querying()
        self.album = self.choosing_album()

    def defining_query(self, query_type):
        if query_type.lower() == "album":
            return ("""
                SELECT
                    album_name,
                    album_url
                FROM
                    `mooncake-304003.wawaweewa.albums` 
                WHERE
                    album_name LIKE "%{}%"
                """.format(self.model_name)
            )
        else:
            return ("""
                SELECT
                    album_name,
                    album_url
                FROM
                    `mooncake-304003.wawaweewa.albums` 
                WHERE
                    model_name LIKE "%{}%"
                """.format(self.model_name)
            )

    def querying(self):
        return self.client.query(self.query)

    def choosing_album(self):
        return random.choice([i for i in self.results])[0:2]

    def __call__(self, *args, **kwargs):
        return '{} - {}:\n\n{}'.format(
            self.model_name.split(' - ')[0],
            self.album[0],
            self.album[1]
        )
