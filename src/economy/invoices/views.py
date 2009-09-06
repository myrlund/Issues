
from economy.invoices.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404

def load_project(project_id):
    project_id = int(project_id)
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        project = Project.objects.create(id=project_id)
    return project

def render_project_response(template, project_id, vars={}, request=None):
    project = load_project(project_id);
    render_to_response("invoices/"+template, vars+{"project": project}, RequestContext(request))

def overview(request, project_id):
    return render_project_response("overview.html", project_id, {"project": project}, request)

def form(request, project_id, model, id=None, parent_field=None, parent_id=None):
    if id:
        object = model.objects.get(id=id)
    elif parent_field and parent_id:
        if parent_field is "project_id":
            parent_id = project_id
        object = model(**{parent_field: parent_id})
    else:
        object = model()
    return render_project_response("form.html", project_id, {"model": model, "object": object}, request)

def show_changes(request, project_id):
    return Http404()

def show_invoices(request, project_id):
    return Http404()
