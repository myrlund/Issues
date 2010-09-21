
from django.conf.urls.defaults import * #@UnusedWildImport
from django.contrib.auth.views import logout, login

urlpatterns = patterns('fokus.user.views',
    url(r'^login/$', login, {'template_name': 'issues/user/login.html'}, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^changepassword/$', 'change_password', name='change_password'),
    
    url(r'^(?:(?P<username>[^/]+)/)?edit/$', 'edit_profile', name='edit_profile'),
    url(r'^(?:(?P<username>[^/]+)/)?$', 'show_profile', name='show_profile'),
)
