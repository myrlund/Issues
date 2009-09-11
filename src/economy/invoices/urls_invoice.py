from django.conf.urls.defaults import *

from economy.invoices.models import Invoice, InvoiceForm

urlpatterns = patterns('economy.invoices.views',
    (r'^$', 'list', {"model": Invoice}),
    (r'^new/$', 'form', {"form_class": InvoiceForm, "model": Invoice}),
    (r'^edit/(?P<number>\d+)/$', 'form', {"form": InvoiceForm}),
    (r'^(?P<number>\d+)/$', 'show', {"model": Invoice}),
                       
#    (r'^$', 'list_invoices'),
#    (r'^new/$', 'invoice_form'),
#    (r'^edit/(?P<number>\d+)/$', 'invoice_form'),
#    (r'^(?P<number>\d+)/$', 'show_invoice'),
)
