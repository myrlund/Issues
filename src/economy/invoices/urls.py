from django.conf.urls.defaults import *

from economy.invoices.models import *

urlpatterns = patterns('economy.invoices.views',
    (r'^$', 'overview'),
    (r'^invoices/$', 'show_invoices'),
    (r'^changes/$', 'show_changes'),
    
    (r'^contract/new/$', 'form',
        {'model': Contract, 'parent_field': 'project_id', 'parent_id': True}),
)
