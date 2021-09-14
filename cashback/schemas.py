import datetime
from typing import List

import pydantic


class Customer(pydantic.BaseModel):
    social_number: str
    name: str


class Product(pydantic.BaseModel):
    type: str
    amount: float
    quantity: int


class Order(pydantic.BaseModel):
    sold_at: datetime.datetime
    customer: Customer
    total_amount: float
    products: List[Product] = []


class Cashback(pydantic.BaseModel):
    createdAt: datetime.datetime
    message: str
    id: str
    document: str
    cashback: str
