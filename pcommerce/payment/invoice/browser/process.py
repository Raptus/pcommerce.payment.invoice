from xml.dom import minidom

from Products.Five.browser import BrowserView

from pcommerce.core.interfaces import IPaymentProcessor, IOrderRegistry
from pcommerce.payment.invoice.plugin import FAILED, SUCCESS

class ProcessInvoice(BrowserView):
    """process Invoice payments
    """

    def __call__(self, orderid, failed=False):
        orderid = int(orderid)
        registry = IOrderRegistry(self.context)
        order = registry.getOrder(orderid)
        if order is not None and order.paymentid == 'pcommerce.payment.invoice':
            order.paymentdata.state = failed and FAILED or SUCCESS
        processor = IPaymentProcessor(self.context)
        return processor.processOrder(orderid, 'pcommerce.payment.invoice')
