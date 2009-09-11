from django.conf.urls.defaults import *

from economy.invoices.models import ChangeForm, Change

urlpatterns = patterns('economy.invoices.views',
    (r'^$', 'list', {"model": Change}),
    (r'^new/$', 'form', {"form_class": ChangeForm, "model": Change}),
    (r'^edit/(?P<number>\d+)/$', 'form', {"form_class": ChangeForm, "model": Change}),
    (r'^(?P<number>\d+)/$', 'show', {"model": Change}),
)
