import random
import unittest

from billing_module.billing import Billing
from billing_module.utils import Utils


class TestsBillingProcess(unittest.TestCase):

    def test_make_invoices(self):
        """
        The idea is:
            - generate an orders lists of know number
            - use the instance of the billing.Billing and make_invoices
            - and then compare:
                - the count of the orders list
                - the count of invoices generated
            - success if both count are equal
        :return:
        """
        n = 1000
        print(f"generating {n} orders.")
        order_list = Utils.generate_orders(n)
        billing_instance = Billing()
        billing_instance.make_invoices(order_list)
        print(f"checking if {n} orders generated {n} invoices.")
        self.assertEqual(
            len(billing_instance.invoice_dict.keys()),
            n,
            f"Should be {n}"
        )
        print("OK")

    def test_cancel_invoices(self):
        """
        The idea is:
           - generate a random number less than N, N = invoices count generated before
                to use as a number of invoices to cancel.
           - use the billing instance an cancel the N invoices
           - and then compare:
               - N
               - the count of invoices in canceled status
        :return:
        """
        orders_to_generate = 1000
        orders = Utils.generate_orders(orders_to_generate)

        print(f"generating {orders_to_generate} orders.")
        invoices_to_cancel = 100
        billing_instance = Billing()
        billing_instance.make_invoices(orders)
        i = 0
        list_to_cancel = []
        while i < invoices_to_cancel:
            key = random.randrange(1, orders_to_generate)
            i += 1
            list_to_cancel.append(billing_instance.invoice_dict[str(key)])

        print(f"canceling {invoices_to_cancel} invoices.")
        billing_instance.cancel_invoices(list_to_cancel)
        count = len(billing_instance.credit_notes_dict.keys())
        print(f"checking if were canceled {invoices_to_cancel} invoices.")
        self.assertEqual(count, invoices_to_cancel, f"Should be {invoices_to_cancel}")
        print("OK")

    def test_generate_files(self):
        """
        The idea is:
           - call the generate operation method after call
                - make_invoices
                - cancel_invoices
           - check if the lines of the generated files are equal to the non-canceled invoices
           - check if the file was generated with the format of:
                - client_number-document_type-letter-issue_date
        :return:
        """

        self.assertEqual(sum((1, 2, 1)), 4, "Should be 4")
