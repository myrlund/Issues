from django.shortcuts import get_object_or_404, render_to_response
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden

from fokus.issue.models import Project, Contract

#########################
# Specialized renderers #
#########################

def render_issue_response(request, tpl, vars={}):
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
# Object getters #
##################

def get_project(project_number):
    project, created = Project.objects.get_or_create(number=project_number)
    project.created = created
    return project 

def get_contract(project_number, contract_code):
    return get_object_or_404(Contract, code=contract_code, project__number=project_number)

#############################
# Automatic user middleware #
#############################

class AuthMiddleware:
    def process_request(self, request):
        self.auto_login(request)
        if not request.user.is_authenticated():
            raise HttpResponseForbidden()
    
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