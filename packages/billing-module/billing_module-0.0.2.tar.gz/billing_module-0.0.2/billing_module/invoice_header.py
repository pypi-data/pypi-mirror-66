from billing_module.client import Client


class InvoiceHeader:

    def __init__(self, issue_date, invoice_number, issue_code, letter, client: Client):
        self.issue_date = issue_date
        self.invoice_number = invoice_number
        self.issue_code = issue_code
        self.letter = letter
        self.client = client
