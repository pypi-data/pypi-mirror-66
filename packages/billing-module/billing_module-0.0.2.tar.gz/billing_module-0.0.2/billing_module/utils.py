import random

from billing_module.client import Client
from billing_module.order import Order
from billing_module.product import Product
from billing_module.product_detail import ProductDetail


class Utils:

    @staticmethod
    def generate_orders(number_of_orders):
        # number_of_orders = 1000
        orders = []
        order_number_i = 1
        client_number_i = 1
        address = "local address for testing"
        identity_type = ["DNI", "CUIT", "ETC"]
        for n in range(number_of_orders):
            order = Order(
                order_number_i,
                Client(
                    client_number_i,
                    f"{address} + client number:{client_number_i} client order:{order_number_i}",
                    "tax_condition",
                    identity_type[random.randrange(0, 3)],
                    random.randrange(1000000, 9999999)
                ),
                ProductDetail(
                    Product(
                        random.randrange(1, 4),
                        f"product{random.randrange(1, 100)}",
                        random.randrange(20, 60)
                    ),
                    random.randrange(1, 5)
                )
            )
            order_number_i += 1
            client_number_i += 1
            orders.append(order)

        return orders

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
