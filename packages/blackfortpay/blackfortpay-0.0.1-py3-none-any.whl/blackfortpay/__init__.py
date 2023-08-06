import os
import json
import requests
from collections import namedtuple


class BlackFortPaymentAPIException(Exception):
    def __init__(self, method, message):
        self.method = method
        self.message = message

    def __str__(self):
        return "%s: %s" % (self.method, self.message)


class BlackFortPaymentAPI:
    api_url = 'https://pay.blackfort.exchange/api/v2/'

    def __init__(self, api_key=os.getenv('BLACKFORT_API_USER_KEY'),
                 api_secret=os.getenv('BLACKFORT_API_SECRET_KEY'),
                 pos_id='default-pos-id', locale='en'):
        self.api_key = api_key
        self.api_secret = api_secret
        self.pos_id = pos_id
        self.locale = locale

    def set_pos_id(self, pos_id):
        self.pos_id = pos_id

    def set_locale(self, locale):
        self.locale = locale

    def send_api_request(self, method, **kwargs):
        params = {
            "locale": self.locale,
            "pos_id": self.pos_id,
            **kwargs,
        }

        response = requests.get(
            "%s%s/" % (self.api_url, method),
            params=params,
            auth=(self.api_key, self.api_secret)
        )

        if response.status_code == 401:
            raise BlackFortPayAPIException(
                '401 UNAUTHORIZED',
                'Please check your API User key and API Secret key'
            )

        obj = response.json(object_hook=lambda d: namedtuple(
            '%sResponse' % method, d.keys())(*d.values()))

        if hasattr(obj, 'err'):
            raise BlackFortPayAPIException(method, obj.err)

        return obj

    def get_rate(self, **kwargs):
        return self.send_api_request('GetRate', **kwargs)

    def start_payment(self, **kwargs):
        return self.send_api_request('StartPayment', **kwargs)

    def check_payment(self, **kwargs):
        return self.send_api_request('CheckPayment', **kwargs)

    def cancel_payment(self, **kwargs):
        return self.send_api_request('CancelPayment', **kwargs)

    def get_currency_list(self):
        return self.send_api_request('GetCurrencyList')

    def get_transactions(self, **kwargs):
        return self.send_api_request('GetTransactions', **kwargs)
