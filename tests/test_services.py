from unittest import mock

import pytest

from cashback import services, models, storages


def build_product(product_type, amount, quantity):
    product = models.Product()
    product.type = product_type
    product.amount = amount
    product.quantity = quantity
    return product


def assert_cashback_percentage(products, cashback_expected):
    total_cashback = services.CashbackService.calculate_cashback(products)
    assert total_cashback == pytest.approx(cashback_expected)


def test_cashback_percentage_for_product_a():
    products_a = [build_product('A', 12, 2), build_product('A', 6.29, 5)]
    assert_cashback_percentage(products_a, 0.5545)


def test_cashback_percentage_for_product_b():
    products_b = [build_product('B', 12, 2), build_product('B', 6.29, 5)]
    assert_cashback_percentage(products_b, 0.6654)


def test_cashback_percentage_for_product_c():
    products_c = [build_product('C', 12, 2), build_product('C', 6.29, 5)]
    assert_cashback_percentage(products_c, 0.49905)


def test_cashback_percentage_for_all_product_types():
    products_c = [build_product('A', 12, 2), build_product('B', 6.29, 5), build_product('C', 82.22, 1)]
    assert_cashback_percentage(products_c, 1.35738)


def test_cashback_service_load_order_should_stops_on_model_validations(cashback_service):
    data = [
        {'total_amount': 10},
        {'products': [{'type': 'E'}]},
        {'total_amount': 10, 'products': [{'type': 'A'}]},
        {'customer': {'social_number': '000.111.000-01'}},
        {'products': [{'type': 'A', 'amount': 10.02, 'quantity': -1}]}
    ]
    for cashback_data in data:
        with pytest.raises(AssertionError):
            _ = cashback_service.load_order(cashback_data)


def test_cashback_service_load_order_success(cashback_service, order_sample_data):
    assert cashback_service.load_order(order_sample_data)


def test_cashback_service_should_stops_if_cashback_storage_fails():
    cashback_storage = mock.MagicMock()
    cashback_storage.add.side_effect = storages.CashbackAddException('')
    order_storage = mock.MagicMock()
    cashback_service = services.CashbackService(cashback_storage, order_storage)
    with pytest.raises(storages.CashbackAddException):
        cashback_service.create_cashback({'total_amount': 0.0})
    assert cashback_storage.add.call_count == 1
    assert not cashback_storage.delete.call_count
    assert not order_storage.add.call_count


def test_cashback_service_should_delete_cashback_if_order_storage_fails():
    cashback_storage = mock.MagicMock()
    order_storage = mock.MagicMock()
    order_storage.add.side_effect = storages.OrderAddException('')
    cashback_service = services.CashbackService(cashback_storage, order_storage)
    with pytest.raises(storages.OrderAddException):
        cashback_service.create_cashback({'total_amount': 0.0})
    assert cashback_storage.add.call_count == 1
    assert cashback_storage.delete.call_count == 1


def test_cashback_service_should_return_the_cashback(cashback_sample_data):
    cashback_storage = mock.MagicMock()
    cashback_storage.add.return_value = cashback_sample_data
    order_storage = mock.MagicMock()
    cashback_service = services.CashbackService(cashback_storage, order_storage)
    cashback = cashback_service.create_cashback({'total_amount': 0.0})
    assert cashback.get('id') == '7'
    assert cashback.get('cashback') == '12'
