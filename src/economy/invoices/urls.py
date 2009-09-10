from django.conf.urls.defaults import *

from economy.invoices.models import *

urlpatterns = patterns('economy.invoices.views',
    (r'^$', 'overview'),
    (r'^invoices/$', 'show_invoices'),
    (r'^changes/$', 'show_changes'),
    
#    (r'^contract/new/$', 'contract_form'),
#    (r'^contract/edit/(?P<contract_code>.+)/$', 'contract_form'),
#    (r'^contract/(?P<contract_code>.+)/$', 'show_contract'),
    
#    (r'^contract/(?P<contract_code>.+)/$', 'show_contract'),
)
