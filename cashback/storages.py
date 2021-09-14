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

    def add(self, social_number, amount):
        url = urllib.parse.urljoin(self.cashback_url, 'api/mock/Cashback')
        resp = requests.post(url, json=dict(document=social_number, cashback=amount))
        if not resp.ok:
            raise CashbackAddException('Fail sending cashback')
        return resp.json()

    @staticmethod
    def delete(cashback_id):
        return cashback_id


class OrderStorage:
    def __init__(self, db):
        self.db = db

    def add(self, order):
        with self.db.new_session() as session:
            session.add(order)
            session.commit()
            return order
