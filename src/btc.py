# -*- coding: utf-8 -*-
import datetime
import requests

url = 'https://api.coinext.com.br:8443/AP/GetL2Snapshot'

payload = '{"OMSId": 1, "InstrumentId": 1, "Depth": 1}'

response = requests.post(url, data=payload).text

buy = {
    'operation': 'buy',
    'price': float(response.split(',')[6]),
    'spread': float(response.split(',')[8]),
    'timestamp': datetime.datetime.today()
}

sell = {
    'operation': 'sell',
    'price': float(response.split(',')[16]),
    'spread': float(response.split(',')[18]),
    'timestamp': datetime.datetime.today()
}

print(buy)
print(sell)
