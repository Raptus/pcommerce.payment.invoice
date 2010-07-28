from zope.interface import implements, Interface
from zope.component import adapts

from pcommerce.core import PCommerceMessageFactory as _
from pcommerce.core.interfaces import IPaymentMethod
from pcommerce.payment.invoice.interfaces import IInvoicePayment

class InvoicePayment(object):
    implements(IPaymentMethod, IInvoicePayment)
    adapts(Interface)
    
    title = _('Invoice')
    description = _('Payment on account')
    icon = '++resource++pcommerce_payment_invoice_icon.gif'
    logo = '++resource++pcommerce_payment_invoice_logo.gif'
    
    def __init__(self, context):
        self.context = context
        
    def verifyPayment(self, order):
        return True
    
    def mailInfo(self, order, lang=None, customer=False):
        data = order.paymentdata
        address = data.as_customer and order.address or data.address
        if customer:
            return _('invoice_mailinfo_customer', default="""Billing address
${address}""", mapping=dict(address=address.mailInfo(self.context.REQUEST, lang, customer)))
        else:
            return _('invoice_mailinfo', default="""Billing address
${address}

To process the invoice payment click the following link
${link}""", mapping=dict(address=address.mailInfo(self.context.REQUEST, lang, customer),
                         link='%s/processInvoice?orderid=%s' % (self.context.absolute_url(), order.orderid)))
