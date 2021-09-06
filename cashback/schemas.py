import datetime
from typing import List

import pydantic


class Customer(pydantic.BaseModel):
    document: str
    name: str


class Product(pydantic.BaseModel):
    type: str
    value: str
    qty: int


class Order(pydantic.BaseModel):
    sold_at: datetime.datetime
    customer: Customer
    total: str
    products: List[Product] = []
