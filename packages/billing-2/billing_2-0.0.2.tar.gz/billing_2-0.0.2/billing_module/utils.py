class Utils:

    @staticmethod
    def percent_vat(code):
        """
        Returns the VAT percent according to code
        :param code:
        :return: float value
        """
        if code == 1:
            return 10.05
        elif code == 2:
            return 21
        elif code == 3:
            return 70

    @staticmethod
    def calculate_vat_value(code, price):
        """
        Return the vat value according to cod and price
        :param code:
        :param price:
        :return: float value
        """
        if code == 1:
            return price * 0.1005
        elif code == 2:
            return price * 0.21
        elif code == 3:
            return price * 0.70

    @staticmethod
    def calculate_net_price(price, quantity):
        """
        Return net price
        :param price:
        :param quantity:
        :return: float value
        """
        return price * quantity

    @staticmethod
    def calculate_sale_price(net_price, vat_value):
        """
        Return sale price
        :param net_price:
        :param vat_value:
        :return: float value
        """
        return net_price + vat_value

    @staticmethod
    def get_all(code, price, quantity):
        """
        Return a dictionary with all the calculations related to an invoice
        :param code:
        :param price:
        :param quantity:
        :return: dict
        """
        vat_value = Utils.calculate_vat_value(code, price)
        net_price = Utils.calculate_net_price(code, quantity)
        vat = Utils.percent_vat(code)
        return {
            "vat_value": vat_value,
            "net_price": net_price,
            "sale_price": net_price + vat_value,
            "vat": vat
        }
