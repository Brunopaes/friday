# -*- coding: utf-8 -*-
import requests


class BTCoin:
    def __init__(self):
        self.url = 'https://api.coinext.com.br:8443/AP/GetL2Snapshot'
        self.payload = '{"OMSId": 1, "InstrumentId": 1, "Depth": 1}'
        self.response = self.requesting()

        self.operation = {
            'operation': [],
            'price': [],
            'spread': [],
        }

    # Used in __init__
    def requesting(self):
        """This function is used to request into api endpoint.

        Returns
        -------
        response : str
            The str api response.

        """
        return requests.post(self.url, data=self.payload).text

    # Used in __call__
    def parse_response(self):
        """This function parses the api response into a dictionary.

        Returns
        -------

        """
        self.operation.get('operation').append('buy')
        self.operation.get('price').append(
            float(self.response.split(',')[6])
        )
        self.operation.get('spread').append(
            float(self.response.split(',')[8])
        )

        self.operation.get('operation').append('sell')
        self.operation.get('price').append(
            float(self.response.split(',')[16])
        )
        self.operation.get('spread').append(
            float(self.response.split(',')[18])
        )

    # Used in __call__
    def sending_message(self):
        """This function sends a telegram message containing buy/sell data.

        Returns
        -------
        msg : str
            Buying/Selling data.

        """
        return 'Compra: R$ {}\nVenda: R$ {}'.format(
            str(self.operation.get('price')[0]),
            str(self.operation.get('price')[1]),
        )

    def __call__(self, *args, **kwargs):
        self.parse_response()

        return self.sending_message()
