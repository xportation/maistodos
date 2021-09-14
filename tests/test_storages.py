import pytest
import responses
from sqlalchemy.exc import IntegrityError

from cashback import storages


def test_cashback_storage_should_throw_when_add_fails():
    with responses.RequestsMock() as mock_requests:
        mock_requests.add(responses.POST, 'http://tmp.com/api/mock/Cashback', status=404)
        with pytest.raises(storages.CashbackAddException):
            cashback_storage = storages.CashbackStorage('http://tmp.com')
            _ = cashback_storage.add('', 0)


def test_cashback_storage_add_successful(cashback_sample_data):
    with responses.RequestsMock() as mock_requests:
        mock_requests.add(responses.POST, 'http://tmp.com/api/mock/Cashback', json=cashback_sample_data, status=201)
        cashback_storage = storages.CashbackStorage('http://tmp.com')
        cashback = cashback_storage.add('', 0)
        assert cashback


def test_cashback_storage_delete():
    cashback_storage = storages.CashbackStorage('http://tmp.com')
    assert cashback_storage.delete(2)


def test_order_storage_add_without_cashback_id_throws(order_storage, order_dao):
    with pytest.raises(IntegrityError):
        assert order_storage.add(order_dao)


def test_order_storage_add(order_storage, order_dao):
    order_dao.cashback_id = 1
    assert order_storage.add(order_dao)
