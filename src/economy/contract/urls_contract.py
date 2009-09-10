from django.conf.urls.defaults import *

urlpatterns = patterns('economy.contract.views',
    (r'^new/$', 'contract_form'),
    (r'^edit/(?P<contract_code>[^/]+)/$', 'contract_form'),
    (r'^(?P<contract_code>[^/]+)/$', 'show_contract'),
    (r'^(?P<contract_code>[^/]+)/invoice/', include('economy.invoices.urls_invoice')),
    (r'^(?P<contract_code>[^/]+)/change/', include('economy.invoices.urls_change')),
)

