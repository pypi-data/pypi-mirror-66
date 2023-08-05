from billing_module.invoice_header import InvoiceHeader
from billing_module.invoice_detail import InvoiceDetail
from billing_module.invoice_footer import InvoiceFooter


class Invoice:

    def __init__(self, invoice_header: InvoiceHeader, invoice_detail: InvoiceDetail,
                 invoice_footer: InvoiceFooter):
        self.invoice_header = invoice_header
        self.invoice_detail = invoice_detail
        self.invoice_footer = invoice_footer
