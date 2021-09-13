import os


def database_url():
    return os.environ.get('DATABASE_URL', 'sqlite:///./storage.db')


def cashback_url():
    return os.environ.get('CASHBACK_URL', 'https://5efb30ac80d8170016f7613d.mockapi.io')
