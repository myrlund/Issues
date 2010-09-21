# -*- coding: utf8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from fokus.issue.helpers import issue_default_tables, get_project, issue_tables,\
    render_project_response
from fokus.issue.models import Issue, IssueType, IssueStatus
from fokus.core.models import User

def list(request, project_number, key, list_by, issues):
    breadcrumb = key
    key.project = get_project(project_number)
    return render_project_response(request, 'project/list_by.html', project_number, locals())

def list_by_status(request, project_number, status_name):
    project = get_project(project_number)
    if status_name == "open":
        status = get_object_or_404(IssueStatus, closed=True)
        issues = project.issue_set.exclude(status=status)
        status = u"Åpen"
    else:
        status = get_object_or_404(IssueStatus, name=status_name)
        issues = project.issue_set.filter(status=status)
    
    category = {
        'title': u'Saker med status: %s' % status,
        'issues': issues,
    }
    
    return issue_tables(request, project_number, categories=[category], vars=locals())

def list_by_type(request, project_number, type_id):
    list_by = "type"
    project = get_project(project_number)
    key = get_object_or_404(IssueType, id=type_id)
    issues = project.get_by_type(key)
    return list(request, project_number, key, list_by, issues)

def list_by_user(request, project_number, username=None):
    project = get_project(project_number)
    if not username:
        return HttpResponseRedirect(project.get_user_url(request.user))
    user = get_object_or_404(User, username=username)
    
    qs = Issue.objects.filter(subscribers=user)
    
    if user == request.user:
        user = u"meg"
    title = u"Saker tilordnet %s" % user
    
    vars = {
        "breadcrumb": {
            "title": title,
            "no_link": True,
        },
        "pagetitle": title,
    }
    
    return issue_default_tables(request, project_number, qs, vars=vars)
