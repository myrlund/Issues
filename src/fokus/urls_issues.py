from django.conf.urls.defaults import * #@UnusedWildImport

urlpatterns = patterns('fokus.issue.views',
    (r'^edit/(?P<project_number>\d+)/', 'project_edit'),
    (r'^(?P<project_number>\d+)/', include('fokus.issue.urls')),
    
    url(r'^$', 'project_overview', name='project_overview'),
)
