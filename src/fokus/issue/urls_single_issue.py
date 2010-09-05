from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('fokus.issue.views',
    url(r'^unsubscribe/(?:(?P<user_id>\d+)/)?$', 'issue_unsubscribe', name='unsubscribe'),
    url(r'^subscribe/(?:(?P<user_id>\d+)/)?$', 'issue_subscribe', name='subscribe'),
    url(r'^notify/(?:(?P<user_id>\d+)/)?$', 'issue_notify', name='notify'),
    url(r'^denotify/(?:(?P<user_id>\d+)/)?$', 'issue_denotify', name='denotify'),
    url(r'^toggle_notify/(?:(?P<user_id>\d+)/)?$', 'issue_toggle_notify', name='toggle_notify'),
)
urlpatterns += patterns('fokus.update.views',
    url(r'^update/save/$', 'update_save'),
    url(r'^update/delete/$', 'update_delete'),
)
