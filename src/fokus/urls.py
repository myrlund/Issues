from django.conf.urls.defaults import * #@UnusedWildImport

from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.PATH_STATIC}),
    (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    (r'', include('fokus.urls_issues')),
)
