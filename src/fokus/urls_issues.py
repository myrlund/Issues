from django.conf.urls.defaults import * #@UnusedWildImport

urlpatterns = patterns('fokus.issue.views.project',
    (r'^edit/(?P<project_number>\d+)/', 'project_edit'),
    (r'^new/$', 'project_new'),
    (r'^(?P<project_number>\d+)(?:-(?P<project_slug>[^/]+))?/', include('fokus.issue.urls')),
    
    url(r'^$', 'project_overview', name='project_overview'),
)
