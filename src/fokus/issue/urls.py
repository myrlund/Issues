from django.conf.urls.defaults import * #@UnusedWildImport

urlpatterns = patterns('fokus.issue.views',
    url(r'^$', 'project.project_home', name='issue_list'),
    (r'^edit/$', 'project.project_edit'),
    
    # RESTful contracts
    (r'^contracts/$', 'contract.contract_list'),
    (r'^contract/new/$', 'contract.contract_new'),
    (r'^contract/edit/(?P<code>[^/]+)/$', 'contract.contract_edit'),
    (r'^contract/delete/$', 'contract.contract_delete'),
    
    (r'^contract/(?P<code>[^/]+)/$', 'contract.contract_home'),
    
    (r'^contract/(?P<code>[^/]+)/', include('fokus.issue.urls_issue')),
    
    # Listings
    (r'^type/(?P<type_id>\d+)/$', 'list.list_by_type'),
    url(r'^status/(?P<status_name>[^/]+)/$', 'list.list_by_status', name='list_by_status'),
    url(r'^user/(?:(?P<username>[^/]+)/)?$', 'list.list_by_user', name='list_by_user'),
    
    url(r'^multistatus/$', 'issuestatus.issues_set_status', name='multistatus'),
)
urlpatterns += patterns('',
    url(r'^search/$', 'fokus.search.views.search', name='search'),
    
    (r'', include('fokus.issue.urls_issue')),
)
