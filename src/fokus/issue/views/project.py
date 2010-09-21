# -*- coding: utf8 -*-

from django.core.urlresolvers import reverse

from fokus.issue.helpers import render_issue_response, get_project,\
    issue_default_tables, redirect, tab
from fokus.issue.models import Project
from fokus.issue.forms import ProjectForm


def project_overview(request):
    projects = Project.objects.all()
    tools = [tab('new project', 'Opprett prosjekt', reverse('fokus.issue.views.project.project_new'))]
    pagetitle = "Alle prosjekter"
    return render_issue_response(request, 'project/list.html', locals())

def project_home(request, project_number, project_slug=None):
    pagetitle = u"%s" % (get_project(project_number))
    
    categories = [
        {
            "title": u"Mine åpne saker",
            "issues": request.user.issue_set.filter(status__closed=False),
        }
    ]
    return issue_default_tables(request, project_number, categories=categories, active_tab=0, vars=locals())

def project_new(request):
    project = Project()
    return project_form(request, project)

def project_edit(request, project_number, slug=None):
    project = get_project(project_number)
    return project_form(request, project)

def project_form(request, project):
    if project.pk: verb = "Rediger %s" % project.title
    else:          verb = "Opprett prosjekt"
    
    if request.POST:
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            return redirect(request, project.get_absolute_url())
    else:
        form = ProjectForm(instance=project)
    
    return render_issue_response(request, "project/form.html", locals()) 
