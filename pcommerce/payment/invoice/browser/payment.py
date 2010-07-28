from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from pcommerce.core.interfaces import IAddressFactory
from pcommerce.payment.invoice.browser.base import InvoiceBase
from pcommerce.payment.invoice.data import InvoicePaymentData

class InvoicePayment(InvoiceBase):
    template = ViewPageTemplateFile('payment.pt')
    
    def validate(self):
        self.errors = {}
        as_customer = self.request.form.get('invoice_address_as_customer', False)
        if not as_customer:
            factory = IAddressFactory(self.request)
            self.errors = factory.validate('invoice_address')
        return len(self.errors) == 0
    
    def process(self):
        self.data = InvoicePaymentData()
        as_customer = self.request.form.get('invoice_address_as_customer', False)
        if not as_customer:
            factory = IAddressFactory(self.request)
            self.data.address = factory.create('invoice_address')
        self.data.as_customer = as_customer
        props = getToolByName(self.context, 'portal_properties').pcommerce_properties
        self.data.pretaxcharge = props.getProperty('invoice_pretaxcharge', 0.0)
        self.data.posttaxcharge = props.getProperty('invoice_posttaxcharge', 0.0)
        return self.data
