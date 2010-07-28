from zope.interface import implements

from Products.Five.browser import BrowserView

from pcommerce.core.interfaces import IPaymentView, IOrder, IShoppingCart

from pcommerce.payment.invoice.data import InvoicePaymentData

class InvoiceBase(BrowserView):
    implements(IPaymentView)
    
    errors = {}
    
    def __init__(self, payment, request):
        self.payment = payment
        self.context = payment.context
        self.request = request
        self.cart = IShoppingCart(self.context)
        self.order = IOrder(self.context)
        self.data = self.order.paymentdata or InvoicePaymentData()
    
    def __call__(self):
        return self.template()
    
    def validate(self):
        return True
    
    def renders(self):
        return True
        
    def process(self):
        return
    
    @property
    def address(self):
        if self.data.as_customer:
            return self.order.address
        return self.data.address
    
    @property
    def address_as_customer(self):
        if self.request.get('invoice_hidden', False):
            return self.request.get('invoice_address_as_customer', False)
        return self.data.as_customer
