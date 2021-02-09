# -*- coding: utf-8 -*-
import requests
import helpers


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

        self.query = """
            INSERT INTO
                `mooncake-304003.DS_Bruno.btc-trader` 
            VALUES
                ("{}", {}, {}, CURRENT_DATETIME("America/Sao_Paulo"))
        """

        helpers.set_path()
        self.client = helpers.start_connection()

    # Used in __init__
    def requesting(self):
        return requests.post(self.url, data=self.payload).text

    # Used in __call__
    def parse_response(self):
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
    def inserting_in_bd(self):
        for i in range(0, 2):
            self.client.query(self.query.format(
                self.operation.get('operation')[i],
                self.operation.get('price')[i],
                self.operation.get('spread')[i])
            )

    # Used in __call__
    def sending_message(self):
        return 'Compra: R$ {}\nVenda: R$ {}'.format(
            str(self.operation.get('price')[0]),
            str(self.operation.get('price')[1]),
        )

    def __call__(self, *args, **kwargs):
        self.parse_response()
        self.inserting_in_bd()

        return self.sending_message()


if __name__ == '__main__':
    BTCoin().__call__()
