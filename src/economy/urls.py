from django.conf.urls.defaults import * #@UnusedWildImport

from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PATH_STATIC}),
    
    (r'^(?P<project_id>\d+)/', include('economy.contract.urls')),
#    (r'^ajax/(?P<project_id>\d+)/', include('economy.invoices.urls'), {'ajax': True}),
    
    url(r'^$', 'economy.contract.views.project_overview', name='project_overview'),
    
    (r'^ajaxupdate/change/setinvoiced/(?P<change_id>\d+)/$', 'economy.invoices.views.set_invoiced'),
    (r'^ajaxupdate/change/setstatus/(?P<change_id>\d+)/$', 'economy.invoices.views.set_status'),
    (r'^ajaxinfo/statusdate/(?P<change_id>\d+)/(?P<status>\d+)/$', 'economy.invoices.views.getstatusdate'),
    (r'^ajaxinfo/changenumber/(?P<contract_id>\d+)/$', 'economy.invoices.views.getchangenumber'),
)
