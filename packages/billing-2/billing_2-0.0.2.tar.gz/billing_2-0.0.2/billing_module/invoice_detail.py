from billing_module.product import Product


class InvoiceDetail:

    def __init__(self, order_number, product: Product, unit_price, vat, quantity, sale_price, net_price, vat_value):
        self.order_number = order_number
        self.product = product
        self.unit_price = unit_price
        self.vat = vat
        self.quantity = quantity
        self.sale_price = sale_price
        self.net_price = net_price
        self.vat_value = vat_value
        self.status = "in_progress"
