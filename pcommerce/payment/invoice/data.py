from pcommerce.core.data import PaymentData

def InvoicePaymentData(as_customer=True, address=None):
    data = PaymentData('pcommerce.payment.invoice')
    data.as_customer = as_customer
    data.address = address
    return data
