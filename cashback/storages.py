import urllib.parse

import requests


class CashbackAddException(Exception):
    def __init__(self, message):
        self.message = message


class OrderAddException(Exception):
    def __init__(self, message):
        self.message = message


class CashbackStorage:
    def __init__(self, cashback_url):
        self.cashback_url = cashback_url

    def add(self, cashback):
        url = urllib.parse.urljoin(self.cashback_url, 'api/mock/Cashback')
        resp = requests.post(url, json=cashback)
        if not resp.ok:
            raise CashbackAddException('Fail sending cashback')
        return resp.json()

    def delete(self, cashback_id):
        return cashback_id
