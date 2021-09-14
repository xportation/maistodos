from unittest import mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from cashback import application

app = application.create_app()


@pytest.fixture
def client():
    return TestClient(app)


def test_add_cashback_empty_body(client):
    response = client.post('/api/cashback')
    assert response.status_code == 422


def test_add_cashback(client, order_sample_dict):
    response = client.post('/api/cashback', json=order_sample_dict)
    assert response.status_code == 201


def test_database_error_return_status_400(client, order_sample_dict):
    mock_order_storage = mock.MagicMock()
    mock_order_storage.add.side_effect = IntegrityError('', '', '', '')

    with app.container.order_storage.override(mock_order_storage):
        response = client.post('/api/cashback', json=order_sample_dict)
        assert response.status_code == 400
