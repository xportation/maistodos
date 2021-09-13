import pytest


@pytest.fixture
def cashback_sample_data():
    return {
        'createdAt': '2021-09-12T13:52:06.435Z',
        'message': 'Cashback criado com sucesso!',
        'id': '7',
        'document': 'ABC',
        'cashback': '12'
    }
