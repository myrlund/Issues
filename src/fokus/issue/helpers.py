# -*- coding: utf8 -*-

from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.core.urlresolvers import reverse

from fokus.issue.models import Project, Contract, Issue, IssueStatus

#########################
# Specialized renderers #
#########################

def redirect(request, to):
    if request.REQUEST.has_key("next"):
        to = request.REQUEST["next"]
    return HttpResponseRedirect(to)

@login_required
def render_issue_response(request, tpl, vars={}):
    vars["breadcrumb"] = breadcrumb(vars)
    return render_to_response("issues/%s" % tpl, vars, RequestContext(request))

def render_project_response(request, tpl, project_number, vars={}):
    vars['project'] = get_project(project_number)
    
    # Update pagetitle
    if not vars.has_key('pagetitle'):
        vars['pagetitle'] = u"%s" % vars['project']
    else:
        vars['pagetitle'] = u"%s - %s" % (vars['project'], vars['pagetitle'])
    
    # Append to breadcrumb
    vars['breadcrumb'] = breadcrumb(vars)
    vars['breadcrumb'].append(vars['project'])
    
    return render_issue_response(request, tpl, vars)

def render_contract_response(request, tpl, project_number, contract_code, vars={}):
    vars['contract'] = get_contract(project_number, contract_code)

    # Append to breadcrumb
    vars['breadcrumb'] = breadcrumb(vars)
    vars['breadcrumb'].append(vars['contract'])

    return render_project_response(request, tpl, project_number, vars)

##################
# Tools and tabs #
##################


def project_tabs(project):
    tabs = [
        tab('list issues', 'Saker', project.get_absolute_url()),
        tab('list contracts', 'Kontrakter', project.get_contracts_url()),
        tab('search', u'Søk', reverse('fokus.search.views.search', args=(project.id, project.slug,))),
    ]
    return tabs

def project_tools(project):
    tools = [
        tab('edit project', 'Rediger prosjekt', project.get_edit_url()),
        tab('new issue', 'Ny sak', project.get_new_issue_url()),
    ]
    return tools


#######################
# Default view setups #
#######################


def issue_default_tables(request, project_number, qs=None, categories=[], active_tab=None, vars={}):
    project = get_project(project_number)
    
    # Load and filter base queryset
    if not qs: qs = Issue.objects.all()
    qs = qs.filter(project=project)
    
    # Load categories from queryset
    categories.append({
        "title": u"Åpne saker",
        "issues": qs.filter(status__closed=False),
    })
    categories.append({
        "title": u"Alle saker",
        "issues": qs.all(),
    })
    
    return issue_tables(request, project_number, categories, active_tab, vars)

def issue_tables(request, project_number, categories=[], active_tab=None, vars={}):
    project = get_project(project_number)
    
    filters = {
        'code': 'contracts__code',
        'status': 'status__name',
        'user': 'subscribers__username',
    }
    for field, q_field in filters.iteritems():
        if request.GET.has_key(field):
            for category in categories:
                category['issues'] = category['issues'].filter(Q(**{q_field: request.GET[field]}))
    
    # Load tabs
    tools = project_tools(project)
    tabs = project_tabs(project)
    if active_tab: tabs[active_tab]["active"] = True
    
    # Load all IssueStatuses
    all_statuses = IssueStatus.objects.all()
    
    if vars.has_key("breadcrumb"):
        print "WTF!?!?!?"
    vars.update(locals())
    
    return render_project_response(request, 'project/issue_tables.html', project_number, vars)


##################
# Object getters #
##################

def get_project(project_number):
    return get_object_or_404(Project, id=project_number)

def get_contract(project_number, contract_code):
    return get_object_or_404(Contract, code=contract_code, project__number=project_number)

#############################
# Automatic user middleware #
#############################

class AuthMiddleware:
    def process_request(self, request):
        self.auto_login(request)
        if not request.user.is_authenticated():
            return HttpResponse(u"Du er ikke logget inn. Vennligst åpne siden på nytt i SuperOffice.")
    
    def auto_login(self, request):
        if request.GET.has_key("username"):
            if request.user.is_authenticated() and request.user.username == request.GET["username"]:
                return
            else:
                user = authenticate(username=request.GET["username"])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return

###################
# Generic helpers #
###################

def breadcrumb(vars): 
    breadcrumb = None
    if vars.has_key('breadcrumb'):
        breadcrumb = vars['breadcrumb']
    elif vars.has_key("pagetitle"):
        breadcrumb = vars['pagetitle']
    if not breadcrumb:
        breadcrumb = []
    if not isinstance(breadcrumb, list):
        breadcrumb = [breadcrumb]
    return breadcrumb

def tab(name, text, href='#', onclick=''):
    return {
        'name': name,
        'text': text,
        'href': href,
        'onclick': onclick,
    }