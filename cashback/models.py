import re
import uuid

import validate_docbr
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Numeric
from sqlalchemy.orm import declarative_base, validates, relationship

Base = declarative_base()

compare_approx = 0.00001


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, default=lambda: str(uuid.uuid4()))
    sold_at = Column(DateTime)
    total_amount = Column(Numeric(scale=2), nullable=False)
    customer = relationship('Customer', backref='order', cascade='all,delete', uselist=False)
    products = relationship('Product', backref='order', cascade='all,delete')

    @validates('total_amount')
    def validate_total_amount(self, _, total_amount):
        if not total_amount:
            total_amount = 0.0

        total = sum([p.total_amount() for p in self.products])
        assert (total_amount - total) < compare_approx, 'Invalid Total Amount'
        return total_amount


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String(36), ForeignKey('order.id'), nullable=False)
    name = Column(String, nullable=False)
    social_number = Column(String, nullable=False)

    @validates('social_number')
    def validate_social_number(self, _, social_number):
        social_number = re.sub('[^0-9]', '', social_number)
        assert validate_docbr.CPF().validate(social_number), 'Invalid Social Number'
        return social_number


class ProductType:
    a = 'A'
    b = 'B'
    c = 'C'

    all_types = [a, b, c]

    @classmethod
    def is_valid(cls, product_type):
        return product_type in cls.all_types


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String(36), ForeignKey('order.id'), nullable=False)
    type = Column(String, nullable=False)
    amount = Column(Numeric(scale=2), nullable=False)
    quantity = Column(Integer, nullable=False)

    @validates('type')
    def validate_type(self, _, product_type):
        product_type = product_type.upper()
        assert ProductType.is_valid(product_type), 'Invalid Product Type'
        return product_type

    @validates('quantity')
    def validate_quantity(self, _, quantity):
        assert quantity >= 0, 'Invalid Product Quantity'
        return quantity

    def total_amount(self):
        if not self.quantity or not self.amount:
            return 0
        return self.quantity * self.amount
