from django.conf.urls.defaults import * #@UnusedWildImport

urlpatterns = patterns('economy.invoices.views',
    # (r'^$', 'overview'),
    (r'^invoice/$', 'show_invoices'),
    (r'^change/$', 'show_changes'),
    
    (r'EA(?P<number>\d+)/$', 'show_change'),
    (r'EA(?P<number>\d+)/edit/$', 'edit_change'),
    (r'(?P<number>\d+)/$', 'show_invoice'),
    (r'(?P<number>\d+)/edit/$', 'edit_invoice'),
    
    (r'change/new/$', 'new_change'),
    (r'invoice/new/$', 'new_invoice'),
    
#    (r'^contract/new/$', 'contract_form'),
#    (r'^contract/edit/(?P<contract_code>.+)/$', 'contract_form'),
#    (r'^contract/(?P<contract_code>.+)/$', 'show_contract'),
    
#    (r'^contract/(?P<contract_code>.+)/$', 'show_contract'),
)
