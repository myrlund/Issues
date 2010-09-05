from django.conf.urls.defaults import * #@UnusedWildImport

urlpatterns = patterns('fokus.issue.views',
    # RESTful issues
    (r'^issue/new/$', 'issue_new'),
    (r'^issue/edit/(?P<issue_id>\d+)/$', 'issue_edit'),
    (r'^issue/delete/$', 'issue_delete'),
    (r'^issue/(?P<issue_id>\d+)/$', 'issue_view'),
    (r'^issue/(?P<issue_id>\d+)/', include('fokus.issue.urls_single_issue')),
)
urlpatterns += patterns('',
    url(r'^search/$', 'fokus.search.views.search', name='search'),
)
