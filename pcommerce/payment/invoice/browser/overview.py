from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from pcommerce.payment.invoice.browser.base import InvoiceBase

class InvoiceOverview(InvoiceBase):
    template = ViewPageTemplateFile('overview.pt')