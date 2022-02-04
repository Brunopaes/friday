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


class Fees:
    def __init__(self, message):
        self.message_text = message.get('message').lower().split(' ')
        self.fees = self.extract_fees()
        self.operation = self.message_text[2]
        self.query = """
            UPDATE
                `mooncake-304003.trading.btc-fees`
            SET
                BOTTOM_FEE = {},
                TOP_FEE = {}
            WHERE 
                OPERATION = "{}"
        """

        self.client = helpers.start_connection()

    # Used in extract_fees
    @staticmethod
    def parse_fees(fees):
        """This function parses fees into numbers.

        Parameters
        ----------
        fees : iterator
            Fees iterator.

        Returns
        -------
        fees : iterator
            Float-parsed fees iterator.

        """
        try:
            return tuple(float(fee) for fee in fees)
        except ValueError:
            return False, False

    # Used in extract_fees
    @staticmethod
    def validate_parsing(fees):
        """This function validates parsing. If fails, raise.

        Parameters
        ----------
        fees : iterator
            Float-parsed fees iterator.

        Returns
        -------
        fees : iterator
            Float-parsed fees iterator.

        """
        if all(fees):
            return fees
        raise ValueError

    # Used in __init__
    def extract_fees(self):
        """This function extracts fees from message text.

        Returns
        -------
        fees : iterator
            Float-parsed fees iterator.

        """
        return self.validate_parsing(self.parse_fees(self.message_text[3:5]))

    # Used in __call__
    def querying(self):
        """This function queries into BQ.

        Returns
        -------

        """
        self.client.query(self.query.format(
            self.fees[0],
            self.fees[1],
            self.operation
        ))

    def __call__(self, *args, **kwargs):
        self.querying()
        return 'Fees were successfully updated!'


class Trade:
    def __init__(self, message):
        self.message_text = message.get('message').lower().split(' ')

        self.username = self.format_user_name(message)
        self.user_id = message.get('sender_id')
        self.price = self.extract_price()

        self.query = """
            INSERT INTO 
                `mooncake-304003.trading.btc-trade` 
            VALUES 
                ({}, "{}", {}, CURRENT_DATETIME("America/Sao_Paulo"))
        """

        self.client = helpers.start_connection()

    # Used in __init__
    @staticmethod
    def format_user_name(message):
        """This function joins user's first and last name.

        Parameters
        ----------
        message : telebot.types.Message.
            Telegram object.

        Returns
        -------
        username : str
            Username.

        """
        return '{} {}'.format(
            message.get('first_name'),
            message.get('last_name'),
        )

    # Used in extract_fees
    @staticmethod
    def parse_fees(price):
        """This function parses prices into numbers.

        Parameters
        ----------
        price : str
            To be parsed price.

        Returns
        -------
        price : float, bool
            Float-parsed price value.

        """
        try:
            return float(price)
        except ValueError:
            return False

    # Used in extract_fees
    @staticmethod
    def validate_parsing(price):
        """This function validates parsing. If fails, raise.

        Parameters
        ----------
        price : float, bool
            Float-parsed price.

        Returns
        -------
        price : float
            Float-parsed price value.

        """
        if isinstance(price, float):
            return price
        raise ValueError

    # Used in __init__
    def extract_price(self):
        """This function extracts fees from message text.

        Returns
        -------
        fees : iterator
            Float-parsed fees iterator.

        """
        return self.validate_parsing(self.parse_fees(self.message_text[2]))

    # Used in __call__
    def querying(self):
        """This function queries into BQ.

        Returns
        -------

        """
        self.client.query(self.query.format(
            self.user_id,
            self.username,
            self.price
        ))

    def __call__(self, *args, **kwargs):
        self.querying()
        return 'Purchase price successfully registered!'
