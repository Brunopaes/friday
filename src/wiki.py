# -*- coding: utf-8 -*-
import wikipedia


def wiki(message_text):
    """This function searches on wikipedia by a given term.

    Parameters
    ----------
    message_text : iterator
        Message input

    Returns
    -------
    response : str
        The wikipedia page summary and url.

    """
    wikipedia.set_lang(
        message_text[1] if message_text[1] in (
            'en', 'pt', 'fr', 'de', 'ru', 'es', 'zh',
            'ja', 'ko', 'it', 'uk', 'sv', 'nl', 'pl'
        ) else 'pt'
    )

    try:
        response = \
            wikipedia.page(wikipedia.search(' '.join(message_text[1:]))[0])
    except wikipedia.exceptions.DisambiguationError:
        return 'Impossible, perhaps the archives are incomplete!'
    except Exception as e:
        e.args
        return 'Impossible, perhaps the archives are incomplete!'

    return '{}\n\n{}'.format(
        response.summary,
        response.url
    )
