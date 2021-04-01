# -*- coding: utf-8 -*-
import requests
import ast


class Jagshemash:
    def __init__(self):
        self.url = 'https://www.abibliadigital.com.br/api/verses/nvi/random'

    # Used in __call__
    def requesting(self):
        """This function requests into bible api.

        Returns
        -------
        versicle : str
            Extracted versicle.

        """
        return self.extract_versicle(
            self.parse_response(requests.get(self.url).content)
        )

    # Used in requesting
    @staticmethod
    def parse_response(content):
        """This function parses the http requisition into a dict.

        Parameters
        ----------
        content : bytes
            Api's response content.

        Returns
        -------
        response_object : dict
            The response dict.

        """
        return ast.literal_eval(content.decode('utf-8'))

    # Used in requesting
    @staticmethod
    def extract_versicle(content):
        versicle_text = content.get(
            'text', 'o senhor é meu pastor e nada me faltará.'
        ).lower().capitalize()
        book = content.get('book').get('name', 'Salmos')
        chapter = content.get('chapter', 23)
        versicle_number = content.get('number', 1)

        return '{}\n{} {}:{}'.format(
            versicle_text, book, chapter, versicle_number
        )

    def __call__(self, *args, **kwargs):
        return self.requesting()
