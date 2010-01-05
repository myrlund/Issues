from django.template import RequestContext
from django.shortcuts import render_to_response

from economy.contract.models import Project, Contract

def get_template_dir(model):
    return model.__name__.lower()+"/"

def load_project(project_id):
    project_id = int(project_id)
    try:
        project = Project.objects.get(id=project_id)
    except:
        project = Project.objects.create(id=project_id)
    return project

def load_contract(contract_code):
    try:
        contract = Contract.objects.get(code=contract_code)
    except:
        contract = None
    return contract

def render_contract_response(template, contract_code, vars={}, request=None):
    contract = load_contract(contract_code)
    vars["contract"] = contract
    return render_project_response(template, contract.project.id, vars, request)

def render_project_response(template, project_id, vars={}, request=None):
    project = load_project(project_id)
    vars["project"] = project
    return render_to_response(template, vars, RequestContext(request))
