from cashback import models, storages


class CashbackService:
    def __init__(self, cashback_storage, order_storage):
        self.cashback_storage = cashback_storage
        self.order_storage = order_storage

    def create_cashback(self, order_data):
        order = self.load_order(order_data)
        cashback_amount = self.calculate_cashback(order.products)
        cashback = self.cashback_storage.add(order.customer.social_number, cashback_amount)
        try:
            order.cashback_id = cashback.get('id')
            self.order_storage.add(order)
            return cashback
        except storages.OrderAddException:
            self.cashback_storage.delete(cashback.id)
            raise

    @staticmethod
    def load_order(order_data):
        order = models.Order()
        order.customer = models.Customer(**order_data.get('customer', {}))
        order.products = [models.Product(**p) for p in order_data.get('products', [])]
        order.total_amount = order_data.get('total_amount')
        order.sold_at = order_data.get('sold_at')
        return order

    @staticmethod
    def calculate_cashback(products):
        cashback_percentage = {
            models.ProductType.a: 0.01,
            models.ProductType.b: 0.012,
            models.ProductType.c: 0.009
        }
        total_cashback = 0.
        for product in products:
            total_cashback += product.total_amount() * cashback_percentage.get(product.type, 0.)
        return total_cashback
