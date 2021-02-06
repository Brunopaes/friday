# -*- coding: utf-8 -*-
from google.cloud import bigquery

import os


def set_path():
    """This function sets settings.json in PATH.

    Returns
    -------

    """
    path = os.path.abspath('gcp-credentials.json')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path


def start_connection():
    return bigquery.Client()


def insert_coke(msg):
    set_path()
    client = start_connection()

    client.query("""
    INSERT INTO
        `mooncake-304003.DS_Bruno.coca-cola` 
    VALUES
        ({}, CURRENT_DATETIME("America/Sao_Paulo"))
    """.format(msg))

    return '{} ml successfully inserted'.format(msg)


def aggregate(msg):
    set_path()
    client = start_connection()

    query_dict = {
        'week': """
            SELECT
                SUM(MILLILITERS) AS SUMMARY,
                CONCAT(EXTRACT(YEAR FROM DATETIME), 
                "-", EXTRACT(WEEK FROM DATETIME)) AS SAFRA
            FROM
                `mooncake-304003.DS_Bruno.coca-cola`
            GROUP BY
                SAFRA
        """
    }

    query_result = [i for i in client.query(query_dict.get(msg))]

    return '{}: {} ml'.format(
        query_result[0].values()[1],
        query_result[0].values()[0],
    )

