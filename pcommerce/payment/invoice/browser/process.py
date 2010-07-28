from xml.dom import minidom

from Products.Five.browser import BrowserView

from pcommerce.core.interfaces import IPaymentProcessor

class ProcessInvoice(BrowserView):
    """process Invoice payments
    """

    def __call__(self, orderid):
        processor = IPaymentProcessor(self.context)
        return processor.processOrder(orderid, 'pcommerce.payment.invoice')
