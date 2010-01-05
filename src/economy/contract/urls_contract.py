from django.conf.urls.defaults import * #@UnusedWildImport

urlpatterns = patterns('economy.contract.views',
    url(r'^new/$', 'contract_form', name='new_contract'),
    url(r'^(?P<contract_code>[^/]+)/edit/$', 'contract_form', name='edit_contract'),
    (r'^(?P<contract_code>[^/]+)/$', 'show_contract'),
    (r'^(?P<contract_code>[^/]+)/', include('economy.invoices.urls')),
    # (r'^(?P<contract_code>[^/]+)/invoice/', include('economy.invoices.urls_invoice')),
    # (r'^(?P<contract_code>[^/]+)/change/', include('economy.invoices.urls_change')),
)

