from django.conf.urls.defaults import *

from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PATH_STATIC}),
    
    (r'^(?P<project_id>\d+)/', include('economy.invoices.urls')),
    (r'^ajax/(?P<project_id>\d+)/', include('economy.invoices.urls'), {'ajax': True}),
    
)
