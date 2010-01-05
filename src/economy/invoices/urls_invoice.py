from django.conf.urls.defaults import * #@UnusedWildImport

from economy.invoices.models import Invoice, InvoiceForm

urlpatterns = patterns('economy.invoices.views',
    (r'^$', 'list', {"model": Invoice}),
    (r'^new/$', 'new_invoice'),
    (r'^edit/(?P<number>\d+)/$', 'form', {"form": InvoiceForm}),
    (r'^(?P<number>\d+)/$', 'show', {"model": Invoice}),
)
