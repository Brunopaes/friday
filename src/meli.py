# -*- coding: utf-8 -*-
import requests
import json


def meli(message_text):
    """This function searches on mercado livre by a given product name.

    Parameters
    ----------
    message_text : iterator
        Message input

    Returns
    -------
    response : str
        The wikipedia page summary and url.

    """
    verbose = False
    if message_text[1] in (
        'mla', 'mlb'
    ):
        verbose = True

    if verbose:
        url = 'https://api.mercadolibre.com/sites/{}/search?q={}'.format(
            message_text[1].upper() if message_text[1] in (
                'mla', 'mlb'
            ) else 'MLB',
            ' '.join(message_text[2:])
        )
    else:
        url = 'https://api.mercadolibre.com/sites/{}/search?q={}'.format(
            message_text[1].upper() if message_text[1] in (
                'mla', 'mlb'
            ) else 'MLB',
            ' '.join(message_text[1:])
        )

    return json.loads(
        requests.get(url).content
    ).get('results')[0].get('permalink')
