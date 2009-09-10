from django.conf.urls.defaults import *

urlpatterns = patterns('economy.contract.views',
    (r'^$', 'list_contracts'),
    (r'^contract/', include('economy.contract.urls_contract')),
)


