import datetime
from unittest import mock

import pytest

from cashback import storages, database, models, services


@pytest.fixture
def cashback_sample_data():
    return {
        'createdAt': '2021-09-12T13:52:06.435Z',
        'message': 'Cashback criado com sucesso!',
        'id': '7',
        'document': 'ABC',
        'cashback': '12'
    }


def build_order_sample(is_raw_mode):
    sold_at = '2021-01-01 00:00:00' if is_raw_mode else datetime.datetime.utcnow()
    return {
        'sold_at': sold_at,
        'total_amount': 46.98,
        'customer': {
            'name': 'Feliciano Santos',
            'social_number': '354.645.572-02'
        },
        'products': [
            {'type': 'A', 'amount': 10.99, 'quantity': 2},
            {'type': 'B', 'amount': 6.25, 'quantity': 4}
        ]
    }


@pytest.fixture
def order_sample_data():
    return build_order_sample(False)


@pytest.fixture
def order_sample_dict():
    return build_order_sample(True)


@pytest.fixture
def cashback_service():
    return services.CashbackService(mock.MagicMock(), mock.MagicMock())


@pytest.fixture
def order_dao(cashback_service, order_sample_data):
    return cashback_service.load_order(order_sample_data)


@pytest.fixture
def db_factory():
    db = database.Database('sqlite://', mock.MagicMock())
    db.create_database(models.Base.metadata)
    return db


@pytest.fixture
def order_storage(db_factory):
    return storages.OrderStorage(db_factory)
