from billing_module.product import Product


class ProductDetail:

    def __init__(self, product: Product, quantity):
        self.product = product
        self.quantity = quantity
