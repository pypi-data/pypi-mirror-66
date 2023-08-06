from billing_module.credit_note_header import CreditNoteHeader
from billing_module.credit_note_footer import CreditNoteFooter


class CreditNote:

    def __init__(self, credit_note_header: CreditNoteHeader, credit_note_footer: CreditNoteFooter):
        self.credit_note_header = credit_note_header
        self.credit_note_footer = credit_note_footer
