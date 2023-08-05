from billing_module.client import Client


class CreditNoteHeader:

    def __init__(self, issue_date, credit_note_number, issue_code, letter, client: Client):
        self.issue_date = issue_date
        self.credit_note_number = credit_note_number
        self.issue_code = issue_code
        self.letter = letter
        self.client = client
