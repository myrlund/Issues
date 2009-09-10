from django.conf.urls.defaults import *

urlpatterns = patterns('economy.invoices.views',
    (r'^$', 'list_invoices'),
    (r'^new/$', 'invoice_form'),
    (r'^edit/(?P<number>\d+)/$', 'invoice_form'),
    (r'^(?P<number>\d+)/$', 'show_invoice'),
)
