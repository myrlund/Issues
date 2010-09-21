# -*- coding: utf8 -*-

from fokus.issue.helpers import render_issue_response, get_project,\
    issue_default_tables
from fokus.issue.models import Project


def project_overview(request):
    projects = Project.objects.all()
    pagetitle = "Alle prosjekter"
    return render_issue_response(request, 'project/list.html', locals())

def project_home(request, project_number):
    pagetitle = u"%s" % (get_project(project_number))
    
    categories = [
        {
            "title": u"Mine åpne saker",
            "issues": request.user.issue_set.filter(status__closed=False),
        }
    ]
    return issue_default_tables(request, project_number, categories=categories, active_tab=0, vars=locals())

def project_edit(request, project_number):
    pass
