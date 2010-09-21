# -*- coding: utf8 -*-
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from fokus.user.forms import LoginForm, ProfileForm
from fokus.issue.helpers import render_issue_response, tab, redirect
from fokus.core.models import User

def show_profile(request, username=None):
    if username:
        user = User.objects.get(username__exact=username)
    else:
        user = request.user
    
    tools = [tab('edit profile', 
                'Rediger profil', 
                reverse('fokus.user.views.edit_profile', args=(user.username,))),
             tab('change password',
                 'Endre passord',
                 reverse('fokus.user.views.change_password'))
            ]
    
    return render_issue_response(request, "user/show_profile.html", locals())

def edit_profile(request, username=None):
    if username:
        user = User.objects.get(username__exact=username)
    else:
        user = request.user
    
    if request.POST:
        form = ProfileForm(request.POST, instance=user)
        
        if form.is_valid():
            user = form.save()
            return redirect(request, reverse('fokus.user.views.show_profile', args=(user.username,)))
    else:
        form = ProfileForm(instance=user)
    
    return render_issue_response(request, "user/edit_profile.html", locals())

def change_password(request):
    raise Http404
