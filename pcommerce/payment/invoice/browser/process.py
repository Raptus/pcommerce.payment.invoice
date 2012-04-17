from xml.dom import minidom

from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

from pcommerce.core import PCommerceMessageFactory as _
from pcommerce.core.interfaces import IPaymentProcessor, IOrderRegistry
from pcommerce.core import config
from pcommerce.payment.invoice.plugin import FAILED, SUCCESS

class ProcessInvoice(BrowserView):
    """process Invoice payments
    """

    def __call__(self, orderid, failed=False):
        orderid = int(orderid)
        registry = IOrderRegistry(self.context)
        order = registry.getOrder(orderid)
        if order is not None and order.paymentid == 'pcommerce.payment.invoice':
            pre_state = order.state
            order.paymentdata.state = FAILED if failed or pre_state is FAILED else SUCCESS
            processor = IPaymentProcessor(self.context)
            result = processor.processOrder(orderid, 'pcommerce.payment.invoice')
            msg = (_('Processing the order failed'), 'error')
            if pre_state is config.PROCESSED or pre_state is config.FAILED:
                msg = (_('Order already processed'), 'error')
            elif failed and order.state is config.FAILED:
                msg = (_('Order successfully canceled'), 'info')
            elif not failed and order.state is config.PROCESSED:
                msg = (_('Order successfully processed'), 'info')
            self.request.response.redirect('%s/order-details?order_id=%s' % (self.context.absolute_url(), orderid))
        else:
            msg = (_('Order not found'), 'error')
            self.request.response.redirect('%s/manage-orders' % self.context.absolute_url())
        IStatusMessage(self.request).add(*msg)
