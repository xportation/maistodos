import pytest
from fastapi.testclient import TestClient

from cashback import application


@pytest.fixture
def client():
    return TestClient(application.create_app())


def test_add_cashback_empty_body(client):
    response = client.post('/api/cashback')
    assert response.status_code == 422


def test_add_cashback(client):
    sample_order_data = {
        'sold_at': '2026-01-02 00:00:00',
        'customer': {
           'social_number': '00000000000',
           'name': 'JOSE DA SILVA',
        },
        'total_amount': '90.00',
        'products': [
           {
              'type': 'B',
              'amount': '10.00',
              'quantity': 9,
           }
        ],
    }
    response = client.post('/api/cashback', json=sample_order_data)
    assert response.status_code == 201
