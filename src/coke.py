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


def insert_coke(milliliters):
    set_path()
    client = start_connection()

    client.query("""
    INSERT INTO
        `mooncake-304003.DS_Bruno.coca-cola` 
    VALUES
        ({}, CURRENT_DATETIME("America/Sao_Paulo"))
    """.format(milliliters))

    return '{} ml successfully inserted'.format(milliliters)
