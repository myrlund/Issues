from django.template import RequestContext
from django.shortcuts import render_to_response

from django.conf import settings 
from economy.contract.models import Project, Contract

def get_template_dir(model):
    return model.__name__.lower()+"/"

def load_project(project_number):
    project_number = int(project_number)
    try:
        project = Project.objects.get(number=project_number)
    except:
        project = Project.objects.create(number=project_number)
    return project

def load_contract(contract_code, project):
    try:
        contract = Contract.objects.get(code=contract_code, project=project)
    except:
        contract = None
    return contract

def render_contract_response(template, contract_code, project_id, vars={}, request=None):
    project = load_project(project_id)
    contract = load_contract(contract_code, project)
    vars["contract"] = contract
    return render_project_response(template, contract.project.id, vars, request)

def render_project_response(template, project_id, vars={}, request=None):
    project = load_project(project_id)
    vars["project"] = project
    return render_to_response(template, vars, RequestContext(request))
