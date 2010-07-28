from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from pcommerce.payment.invoice.browser.base import InvoiceBase

class InvoiceConfirmation(InvoiceBase):
    template = ViewPageTemplateFile('confirmation.pt')