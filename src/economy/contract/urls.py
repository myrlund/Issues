from django.conf.urls.defaults import * #@UnusedWildImport

from economy.contract.views import list_contracts

urlpatterns = patterns('economy.contract.views',
    url(r'^$', list_contracts, name='project'),
    (r'^new/$', 'new_contract',),
    (r'^(?P<contract_code>[^/]+)/edit/$', 'edit_contract'),
    (r'^(?P<contract_code>[^/]+)/$', 'show_contract'),
    (r'^(?P<contract_code>[^/]+)/', include('economy.invoices.urls')),
)


