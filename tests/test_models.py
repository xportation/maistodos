import pytest

from cashback import models


def test_invalid_customer_social_number():
    invalid_social_numbers = ['', '111.222.000-80', '58070424172', '154.645.572-02', '54.645.572-02', '253.135.632-033']
    for social_number in invalid_social_numbers:
        with pytest.raises(AssertionError, match='Invalid Social Number'):
            customer = models.Customer()
            customer.social_number = social_number


def test_customer_social_number_can_be_formatted_or_not():
    expected_social_number = '35464557202'
    social_numbers = ['354.645.572-02', '35464557202', '354645572-02']
    for social_number in social_numbers:
        customer = models.Customer()
        customer.social_number = social_number
        assert customer.social_number == expected_social_number


def test_invalid_product_type():
    for product_type in ['a', 'b', 'c', 'D', 'd', '1', '2', '3']:
        assert not models.ProductType.is_valid(product_type)


def test_product_type_validation():
    for product_type in ['D', 'd', '1', '2', '3']:
        with pytest.raises(AssertionError, match='Invalid Product Type'):
            product = models.Product()
            product.type = product_type


def test_product_type_can_be_lower_case():
    for product_type in ['a', 'b', 'c']:
        product = models.Product()
        product.type = product_type
        assert product.type == product_type.upper()


def test_product_quantity_can_not_be_negative():
    for quantity in [-999999999, -1]:
        with pytest.raises(AssertionError, match='Invalid Product Quantity'):
            product = models.Product()
            product.quantity = quantity


def test_product_quantity_must_be_zero_or_positive_values():
    for quantity in [0, 1, 9999999]:
        product = models.Product()
        product.quantity = quantity


def test_product_total_amount():
    product = models.Product()
    product.quantity = 0
    product.amount = 10.02
    assert product.total_amount() == pytest.approx(0)

    product.quantity = 3
    assert product.total_amount() == pytest.approx(30.06)

    product.amount = 4.10
    assert product.total_amount() == pytest.approx(12.3)


def test_product_total_amount_is_zero_if_not_quantity_or_amount():
    product = models.Product()
    assert product.total_amount() == pytest.approx(0)

    product.quantity = 3
    assert product.total_amount() == pytest.approx(0)

    product.quantity = 0
    product.amount = 4.10
    assert product.total_amount() == pytest.approx(0)


def build_product(amount, quantity):
    product = models.Product()
    product.amount = amount
    product.quantity = quantity
    return product


def test_order_must_validate_wrong_total_amount():
    products = [build_product(10.02, 3), build_product(4.1, 2), build_product(99.99, 1)]
    order = models.Order()
    order.products = products
    order.total_amount = 138.25
    with pytest.raises(AssertionError, match='Invalid Total Amount'):
        order.total_amount = 138.26


def test_order_total_amount_is_zero_when_none():
    order = models.Order()
    order.total_amount = None
    assert order.total_amount == pytest.approx(0)
