import datetime
from typing import List

import pydantic


class Customer(pydantic.BaseModel):
    social_number: str
    name: str


class Product(pydantic.BaseModel):
    type: str
    amount: str
    quantity: int


class Order(pydantic.BaseModel):
    sold_at: datetime.datetime
    customer: Customer
    total_amount: str
    products: List[Product] = []
